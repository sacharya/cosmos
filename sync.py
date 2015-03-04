from app import app
from app.db import dbapi
from config import config
from glanceclient import Client
from keystoneclient.v3 import client as keystonev3_api

auth_urls_v3 = config.get('auth_url_v3')

while True:
  print "\nStarting sync"
  service_username = config.get('service').get('username')
  password = config.get('service').get('password')

  trusts_from_db = dbapi.get_all_trusts()
  print "Trusts from db %s " % len(trusts_from_db)

  print "Total regions %s " % len(auth_urls_v3)
  trusts_from_api = []
  for region, keystone_url in auth_urls_v3.iteritems():
    print "\n\nKeystone url %s " % keystone_url
    trustee = keystonev3_api.Client(
        username=service_username, password=password,
        auth_url=keystone_url)
    
    trusts_from_api =trustee.trusts.list(trustee_user=trustee.user_id)
    print "Trusts from api %s " % len(trusts_from_api)

    # admin_required
    #endpoints = trustee.service_catalog.url_for(service_type='image')
    
    endpoints = trustee.service_catalog.get_endpoints(service_type='image')
    glance_endpoint = ""
    for endpoint in endpoints.iterkeys():
      for image_endpoints in  endpoints[endpoint]:
        for field in image_endpoints.iterkeys():
          if image_endpoints[field] == 'public':
            glance_endpoint =  image_endpoints[u'url']
            break
    print "Glance endpoint %s " % glance_endpoint

    for dtrust in trusts_from_db:
      for atrust in trusts_from_api:
        if atrust.id == trust.trust_id:
          print "Sync started for trust id %s " % trust.trust_id
          glance = Client('1', endpoint=glance_endpoint, token=trustee.auth_token)
          images = glance.images.list()
          for image in images:
            print image
  print "Sync complete"
