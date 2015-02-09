from config import config
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from app import app

from keystoneclient.v2_0 import client as keystone_api
from keystoneclient.v3 import client as keystonev3_api
from keystoneclient.openstack.common.apiclient.exceptions import Unauthorized

from novaclient.v1_1 import client as nova_api

auth_url_v2 = config.get('default', 'auth_url_v2')
auth_url_v3 = config.get('default', 'auth_url_v3')

@app.route('/index')
def index():
  return render_template("index.html", title="Home")

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template("login.html", title="Login")
  username = request.form.get('username')
  password = request.form.get('password')
  remember_me = request.form.get('remember_me')
  try:
    keystone = keystonev3_api.Client(username=username, password=password, auth_url=auth_url_v3) 
    session['username'] = keystone.username
    session['token'] = keystone.auth_token
    session['tenant_id'] = keystone.tenant_id
    session['user_id'] = keystone.user_id
  except Unauthorized as e:
    print e
    flash("Invalid username or passord.")
    return redirect(url_for('login'))
  return redirect(url_for('delegate'))

@app.route('/delegate')
def delegate():
  if 'username' not in session:
    flash("Unauthenticated user.")
    return redirect(url_for('login'))
  
  username = config.get('service', 'username')
  password = config.get('service', 'password')
  auth_url_v31 = config.get('service', 'auth_url_v3')
  compute_url = config.get('service', 'compute_url')

  trustee = keystonev3_api.Client(username=username, password=password, auth_url=auth_url_v31)
  
  token = session['token']
  truster = keystonev3_api.Client(token=token, auth_url=auth_url_v3)
  trust = truster.trusts.create(trustee.user_id, session['user_id'], role_names=['Member'], project=truster.tenant_id, impersonation=True)

  bypass_url = compute_url + truster.project_id
  trustee_new = keystonev3_api.Client(username=trustee.username, token=trustee.auth_token, trust_id=trust.id, auth_url=auth_url_v31)

  nova = nova_api.Client(auth_token=trustee_new.auth_token, bypass_url=bypass_url)
  servers = nova.servers.list()
  return "Delegation is workin"

