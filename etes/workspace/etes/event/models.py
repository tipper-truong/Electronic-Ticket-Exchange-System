"""
Model for Events
Database representation for individual events
"""

from etes import db# Shared project DB

"""
    An Event Object Model
"""
class Event(db.Model):

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    venue = db.Column(db.String(100))
    location = db.Column(db.String(100))
    date = db.Column(db.String(100))
    starttime = db.Column(db.String(100))
    endtime = db.Column(db.String(100))
    imgpath = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Numeric(precision=2))
    quantity = db.Column(db.Integer())
    
    tickets = db.relationship('Ticket', backref='event', lazy='dynamic')

    def __init__(self, name, genre, venue, location, date, starttime, endtime, imgpath, user, price, quantity):
        self.imgpath = imgpath
        self.name = name
        self.genre = genre
        self.venue = venue
        self.location = location
        self.date = date
        self.starttime = starttime
        self.endtime = endtime
        self.user_id = user.id
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        # Similar to a toString method of Java
        return '<Event %r>' % self.name

"""
    A Ticket Object Model that stores on the bought tickets from the user
"""
class Ticket(db.Model):
    
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.Integer())
    country = db.Column(db.String(100))
    cardnum = db.Column(db.String(100))
    expiry = db.Column(db.String(100))
    cvv = db.Column(db.Integer)
    timestamp = db.Column(db.String(100))
    bought = db.Column(db.Integer())
    
    # event = db.relationship('Event', backref='ticket', lazy='dynamic')
    
    def __init__(self, event_id, seller_id, buyer_id, fname, lname, phone, street, city, state, zip, country, cardnum, expiry, cvv, timestamp, bought):
        self.event_id = event_id
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.cardnum = cardnum
        self.expiry = expiry
        self.cvv = cvv
        self.timestamp = timestamp
        self.bought = bought
    
    def __repr__(self):
        # Similar to a toString method of Java
        return '<Ticket %r>' % self.fname
    
        
    