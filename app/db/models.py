from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    tenant_id = db.Column(db.String(80))
    user_id = db.Column(db.String(80))
    default_auth_url = db.Column(db.String(80))
    trusts = db.relationship('Trust', backref='user')

    def __init__(self, username, tenant_id, user_id, default_auth_url):
        self.username = username
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.default_auth_url = default_auth_url
    def __repr__(self):
        return '<Username %s. Tenant ID %s. Keystone %s.>' % (self.username, self.tenant_id, self.default_auth_url)

    def is_authenticated(self):
        return True

class Keystone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_url = db.Column(db.String(80))

    def __init__(self, auth_url):
        self.auth_url = auth_url

class Trust(db.Model):
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    keystone_fk = db.Column(db.Integer, db.ForeignKey('keystone.id'), primary_key=True)
    trust_id = db.Column(db.String(80), unique=True)
    keystone = db.relationship('Keystone', backref='trusts')

    def __repr__(self):
        return '<Trust ID %s. User ID %s. Keystone ID %s.>' % (self.trust_id, self.user_fk, self.keystone_fk)
