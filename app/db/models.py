from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    tenant_id = db.Column(db.String(80))
    user_id = db.Column(db.String(80))

    def __init__(self, username, tenant_id, user_id):
        self.username = username
        self.tenant_id = tenant_id
        self.user_id = user_id
             
    def __repr__(self):
        return '<Username %s. Tenant ID %s. User ID %s>' % (self.username, self.tenant_id, self.user_id)

    def is_authenticated(self):
      return True


class Trust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trustor_username = db.Column(db.String(80))
    trustee_username = db.Column(db.String(80))
    trust_id = db.Column(db.String(80), unique=True)

    def __init__(self, trustor_username, trustee_username, trust_id):
        self.trustor_username = trustor_username
        self.trustee_username = trustee_username
        self.trust_id = trust_id

    def __repr__(self):
        return '<Trustor User %s. Trustee User %s. Trust ID %s>' % (self.trustor_username, self.trustee_username, self.trust_id)
