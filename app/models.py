from app import db


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
