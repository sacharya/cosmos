from app import db
from models import Trust
from models import User


def save_trust(trustor_username, trustee_username, trust_id):
    t = Trust(trustor_username=trustor_username,
              trustee_username=trustee_username,
              trust_id=trust_id)
    db.session.add(t)
    db.session.commit()


def get_all_trusts_by_trustor(trustor_username):
    return Trust.query.filter_by(trustor_username=trustor_username).all()


def create_or_get_user(username, tenant_id, user_id, default_region, default_auth_url):
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

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
