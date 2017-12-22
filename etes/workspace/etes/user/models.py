"""
    Creating a User Model
"""
from etes import db #importing the database

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35))
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(80))
    address = db.Column(db.String(80))
    
    #Lazy -> means that when you do a look up, you don't fetch all the events unless you explicitly ask for them
    events = db.relationship('Event', backref='user', lazy='dynamic')
     
    def __init__(self, fullname, email, username, password, address):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.address = address
       
    def __repr__(self):
        #Similar to a toString method of Java
        return '<Author %r>' % self.username
     