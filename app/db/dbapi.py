from app import db
from models import Trust
from models import User
from models import Keystone

def get_all_trusts_by_trustor(trustor_username):
    return Trust.query.filter_by(trustor_username=trustor_username).all()

def create_or_get_user(username, tenant_id=None, user_id=None, default_region=None, default_auth_url=None):
    u = User.query.filter_by(username=username, 
                             default_auth_url=default_auth_url).first()
    if u == None:
        u = User(username=username, 
                 tenant_id=tenant_id, 
                 user_id=user_id, 
                 default_region=default_region,
                 default_auth_url=default_auth_url)
        db.session.add(u)
        db.session.commit()
    return u

def create_or_get_keystone(auth_url):
    k = Keystone.query.filter_by(auth_url=auth_url).first()
    if k == None:
        k = Keystone(auth_url=auth_url)
        db.session.add(k)
        db.session.commit()
    return k

def save_trust(trust_id=None, keystone=None, trustor_user=None, trustee_username=None):
    t = Trust.query.filter_by(keystone=keystone, 
                              user=user, 
                              trustor_username=trustor_username, 
                              trustee_username=trustee_username).first()

    if t == None:
        t = Trust(trust_id=trust_id, 
                trustor_username=trustor_username, 
                trustee_username=trustee_username)
        t.keystone = keystone
        t.user = user
        user.trusts.append(t)

        db.session.add(t)
        db.session.add(user)
        db.session.commit()
    return t

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
