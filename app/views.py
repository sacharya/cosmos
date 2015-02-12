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

auth_url_v2 = config.get('default', 'auth_url_v2')
auth_url_v3 = config.get('default', 'auth_url_v3')


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
        return render_template("login.html", title="Login")
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = request.form.get('remember_me')
    try:
        keystone = keystonev3_api.Client(
            username=username, password=password, auth_url=auth_url_v3)
        session['username'] = keystone.username
        session['token'] = keystone.auth_token
        session['tenant_id'] = keystone.tenant_id
        session['user_id'] = keystone.user_id
        dbapi.save_or_update_user(
            keystone.username, keystone.tenant_id, keystone.user_id)
    except Unauthorized as e:
        print e
        flash("Invalid username or passord.")
        return redirect(url_for('login'))
    return redirect(url_for('setup'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/setup')
@login_required
def setup():
    username = config.get('service', 'username')
    auth_url_v3 = config.get('service', 'auth_url_v3')
    compute_url = config.get('service', 'compute_url')
    trustee = {}
    trustee['username'] = username
    trustee['auth_url_v3'] = auth_url_v3
    trustee['compute_url'] = compute_url

    return render_template("setup.html", trustee=trustee)


@app.route('/trust', methods=['POST'])
@login_required
def create_trust():
    username = config.get('service', 'username')
    password = config.get('service', 'password')
    auth_url_v3 = config.get('service', 'auth_url_v3')
    compute_url = config.get('service', 'compute_url')

    trustee = keystonev3_api.Client(
        username=username, password=password, auth_url=auth_url_v3)

    token = session['token']
    print token
    trustor = keystonev3_api.Client(token=token, auth_url=auth_url_v3)
    trust = trustor.trusts.create(trustee.user_id, session['user_id'],
                                  role_names=['Member'],
                                  project=trustor.tenant_id,
                                  impersonation=True)

    dbapi.save_trust(session['username'], trustee.username, trust.id)
    return redirect(url_for('trusts'))


@app.route('/trusts', methods=['GET'])
@login_required
def trusts():
    username = session['username']
    trusts = dbapi.get_all_trusts_by_trustor(username)
    return render_template("trusts_list.html", trusts=trusts)
