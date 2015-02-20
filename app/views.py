from app import app
from app.db import dbapi
from config import config
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from functools import wraps

from keystoneclient.v2_0 import client as keystone_api
from keystoneclient.v3 import client as keystonev3_api
from keystoneclient.openstack.common.apiclient.exceptions import Unauthorized

from novaclient.v1_1 import client as nova_api

auth_urls_v2 = config.get('auth_url_v2')
auth_urls_v3 = config.get('auth_url_v3')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Unauthenticated user.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/index')
def index():
    return render_template("index.html", title="Home")


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('trusts'))
        return render_template("login.html", 
                            title="Login", 
                            auth_urls_v3=auth_urls_v3, 
                            default_region=config.get('default_region'))
    username = request.form.get('username')
    password = request.form.get('password')
    default_region = request.form.get('region')
    remember_me = request.form.get('remember_me')
    keystone_login_url = auth_urls_v3[default_region]

    try:
        default_keystone = keystonev3_api.Client(
            username=username, password=password, auth_url=keystone_login_url)
        session['username'] = default_keystone.username
        session['token'] = default_keystone.auth_token
        session['tenant_id'] = default_keystone.tenant_id
        session['user_id'] = default_keystone.user_id
        session['default_region'] = default_region
        session['tokens_by_url'] = {keystone_login_url: default_keystone.auth_token}
        dbapi.create_or_get_user(
            default_keystone.username, default_keystone.tenant_id, default_keystone.user_id, default_region, keystone_login_url)
    except Unauthorized as e:
        print e
        flash("Invalid username or passord.")
        return redirect(url_for('login'))

    for region, keystone_url in auth_urls_v3.iteritems():
        if keystone_url not in session['tokens_by_url'].keys():
            try:
                keystone = keystonev3_api.Client(username=username, 
                                    password=password, 
                                    auth_url=keystone_login_url)
                session['token_by_url'][keystone_url] = keystone.auth_token
            except Unauthorized as e:
                session['token_by_url'][keystone_url] = "UNAUTHORIZED"

    return redirect(url_for('setup'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/setup') 
@login_required
def setup():
    username = config.get('service').get('username')
    compute_urls = config.get('compute_url')
    region = session.get('default_region')
    trustee = {}
    trustee['username'] = username
    trustee['auth_urls_v3'] = auth_urls_v3
    trustee['compute_urls'] = compute_urls

    return render_template("setup.html", trustee=trustee)


@app.route('/trust', methods=['POST'])
@login_required
def create_trust():
    username = config.get('service').get('username')
    password = config.get('service').get('password')
    region = session.get('default_region')
    default_auth_url = auth_urls_v3.get(region)

    current_user = dbapi.create_or_get_user(session.get('username'), default_auth_url=default_auth_url)

    for region, keystone_url in auth_urls_v3.iteritems():
        trustee = keystonev3_api.Client(
            username=username, password=password, auth_url=keystone_url)

        token = session['tokens_by_url'][keystone_url]
        trustor = keystonev3_api.Client(token=token, auth_url=keystone_url)
        trust = trustor.trusts.create(trustee.user_id, trustor.user_id,
                                      role_names=['human'],
                                      project=trustor.tenant_id,
                                      impersonation=True)
        k = dbapi.create_or_get_keystone(keystone_url)
        dbapi.save_trust(trust_id=trust.id, keystone=k, user=current_user)
    return redirect(url_for('trusts'))


@app.route('/trusts', methods=['GET'])
@login_required
def trusts():
    username = session['username']
    region = session.get('default_region')
    default_auth_url = auth_urls_v3.get(region)

    current_user = dbapi.create_or_get_user(username, default_auth_url=default_auth_url)
    trusts = current_user.trusts

    return render_template("trusts_list.html", trusts=trusts)
