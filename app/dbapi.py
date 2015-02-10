from app import db
from models import Trust

def save_trust(trustor_username, trustee_username, trust_id):
  t = Trust(trustor_username=trustor_username,
      trustee_username=trustee_username,
      trust_id=trust_id)
  db.session.add(t)
  db.session.commit()

def get_all_trusts_by_trustor(trustor_username):
  #return Trust.query.all()
  return Trust.query.filter_by(trustor_username=trustor_username).all()
