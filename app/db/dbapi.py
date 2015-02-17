from app import db
from models import Trusts
from models import User


def save_trust(trustor_username, trustee_username, trust_id):
    t = Trust(trustor_username=trustor_username,
              trustee_username=trustee_username,
              trust_id=trust_id)
    db.session.add(t)
    db.session.commit()


def get_all_trusts_by_trustor(trustor_username):
    return Trust.query.filter_by(trustor_username=trustor_username).all()


def save_or_update_user(username, tenant_id, user_id):
    u = User(username=username, tenant_id=tenant_id, user_id=user_id)
    db.session.add(u)
    db.session.commit()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
