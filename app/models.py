from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Registration.query.get(int(id))

class Registration(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<Registration {}>'.format(self.username)
        
class FurduModel(db.Model):
    name = db.Column(db.String(64), index=True, unique=True, primary_key = True)#roomname by login
    ins = db.Column(db.Integer)
    outs = db.Column(db.Integer)
    
    def __repr__(self):
        return '<FurduModel {}>'.format(self.name)
