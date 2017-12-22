from etes import app
from flask import render_template, redirect, flash, url_for, session, request
from werkzeug.utils import secure_filename
from user.form import RegisterForm, LoginForm
from event.form import SellForm
from etes import db
from event.models import Event, Ticket
from user.models import User
from decimal import *
import os
import uuid
from sqlalchemy.sql import table, column, select, update, insert
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
import re
from operator import itemgetter


@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        # print("stuff")
        # assert app.debug == False
        # return "POST" + request.form
        pass
    else:
        # GET request
        usernames = [u.username for u in User.query.all()]
        if session.get('username') in usernames:  # User is signed in
            
            event = Event.query.all()
            
            # Order date by descending
            
            for ev in event:
                ev.isodate = isodate(re.search('(([0-9]+/?)+)',ev.date).group(0))

            # print(event)
            print(sorted(event, key=get('isodate')))
            
            
            #events = Event.query.order_by(Event.date.desc())  # For displaying based on what tickets the user is selling and displaying events by date in descending order
            
            
            
            user = User.query.filter_by(username=session['username']).first()
            return render_template('event/home.html', event=Event.query.all(), tickets=Ticket.query.all(), user=user)
        else:
            # Preferably an actual template...
            return """
            <meta http-equiv="refresh" content="5;url=/login" />
            <p>Please log first. You'll be redirected in 5 seconds, or click <a href="/login">here</a>!</p>
            """


@app.route('/login')
def logout():
  #Delete the sessions for username when the user logout
  session.pop('username', None)
  regform = RegisterForm()
  form = LoginForm()
  return render_template('user/login.html', form=form, regform=regform)


@app.route('/sell', methods=('GET', 'POST'))
def sell():
  form = SellForm() 
  if form.validate_on_submit():
    #Save image to static/images
    app.config['UPLOAD_FOLDER'] = 'static/images'
    file = request.files.get('imgpath')
    extension = os.path.splitext(file.filename)[1]
    f_name = str(uuid.uuid4()) + extension #encoding the image name + adding extension like jpg, png etc.
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name)) #saving the image to static/images
    event = Event(
        form.name.data,
        form.genre.data,
        form.venue.data,
        form.location.data,
        form.date.data,
        form.starttime.data,
        form.endtime.data,
        "static/images/"+f_name,
        User.query.filter_by(username=session['username']).first(),
        form.price.data,
        form.quantity.data)
   
    db.session.add(event)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('event/sell.html',form=form)


@app.route('/confirmation/<int:event_id>', methods=['POST', 'GET'])
def confirmation(event_id):
    event = Event.query.filter_by(event_id=event_id).first()
    user = User.query.filter_by(username=session['username']).first()
    print (request.method + " REQUEST_METHOD")
    if request.method == 'GET':
        # Get user and event details
        user = User.query.filter_by(username=session['username']).first().__dict__
        event = Event.query.filter_by(event_id=event_id).first()
        name = user['fullname'].split(' ')
        # Make things easier and pre process/parse user info
        user.update(dict(
            firstname=name[0],
            lastname=name[1],
            address=parseaddr(user['address']),
        ))
        # gimme yer monies
        commission = round(Decimal(event.price * Decimal(0.05)), 2)
        shipping = round(Decimal(5.00), 2)
        total = round(event.price + commission + shipping, 2)
        pricing = dict(
            commission=commission,
            shipping=shipping,
            total=total,
        )
        return render_template('user/confirmation.html', user=user, pricing=pricing, event=event)
    if (request.method == 'POST'):
        # verify form
        # insert into tickets
        # redirect to order /status/event_id
        """
       +-----------+----------+-----------+----------+--------+--------+--------+--------------+--------------+---------------+-------+-------+---------------+-----------+--------+------+
| ticket_id | event_id | seller_id | buyer_id | bought | fname  | lname  | phone        | street       | city          | state | zip   | country       | cardnum   | expiry | cvv  |
+-----------+----------+-----------+----------+--------+--------+--------+--------------+--------------+---------------+-------+-------+---------------+-----------+--------+------+
|         4 |       19 |         3 |        2 |        | Tipper | Truong | 415 123 4567 | 574 22nd Ave | San Francisco | CA    | 94121 | United States | 123456790 | Apr/20 | 456  |
+-----------+----------+-----------+----------+--------+--------+--------+--------------+--------------+---------------+-------+-------+---------------+-----------+--------+------+
        """
        print (request.form['first_name'])
        print (request.form['last_name'])
        print (request.form['telephone'])
        print (request.form['address'])
        print (request.form['city'])
        print (request.form['state'])
        print (request.form['zip'])
        print (request.form['country_list'])
        print (request.form['card_number'])
        print (request.form['exp_month'])
        print (request.form['exp_year'])
        print (request.form['cvv'])
    
        ticket = Ticket(
        Event.query.filter_by(event_id=event_id).first(),
        event.user_id,
        User.query.filter_by(username=session['username']).first(),
        request.form['first_name'],
        request.form['last_name'],
        request.form['telephone'],
        request.form['address'],
        request.form['city'],
        request.form['state'],
        request.form['zip'], 
        request.form['country_list'], 
        request.form['card_number'],
        request.form['exp_month'] + '/' + request.form['exp_year'],
        request.form['cvv'])
        
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('status', event_id=event_id))
    return render_template('user/confirmation2.html')
        
        


@app.route('/about')
def about():
    return render_template('event/about.html')


 
@app.route('/status/<int:event_id>',  methods=['GET', 'POST'])
def status(event_id):
    distance = 0
    usr = User.query.filter_by(username=session['username']).first()
    event = Event.query.filter_by(event_id=event_id).first()
    buyeraddr = usr.address
    selleraddr = event.user.address #gets the seller address
    
    # Calculate the distance between buyeraddr and selleraddr
    geolocator = GoogleV3()
    print (buyeraddr + " buyer address")
    print (selleraddr + " seller address")
    
    buyerlocation = geolocator.geocode(buyeraddr)
    sellerlocation = geolocator.geocode(selleraddr)
 
    buyer_lat_lon = (buyerlocation.latitude, buyerlocation.longitude)
    seller_lat_lon = (sellerlocation.latitude, sellerlocation.longitude)
    distance = round(vincenty(buyer_lat_lon, seller_lat_lon).miles)
    
    #event.user_id = usr.id  #After buying ticket, change the owner of the ticket from seller to buyer
    event.quantity -= 1 #decrement quantity
    db.session.commit()
    print ("Buyer:{}\nSeller:{}".format(buyeraddr, selleraddr))
    return  render_template('user/status.html', usr=usr, selleraddr=selleraddr, buyeraddr=buyeraddr, distance=distance)


@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit(event_id):
    event = Event.query.filter_by(event_id=event_id).first_or_404()
    form = SellForm(obj=event)
    f_name = ""
    extension = ""
    app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/images/'
    if form.validate_on_submit():
        original_image = event.imgpath
        form.populate_obj(event)
        # Handle event image uploads
        if form.imgpath.has_file():
            f = request.files.get('imgpath')
            try:
                extension = os.path.splitext(f.filename)[1]
                f_name = str(uuid.uuid4()) + extension #encoding the image name + adding extension like jpg, png etc.
                f_path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
                f.save(f_path) #saving the image to static/images
                event.imgpath = '/static/images/' + f_name
            except:
                flash("The image was not uploaded")
                event.imgpath = original_image # "static/images/"+f_name
        # Commit changes to event and return to homepage
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event/edit.html', form=form, event=event, action="edit")


@app.route('/index/<int:event_id>', methods=['GET', 'POST'])
def delete(event_id):
    event = Event.query.filter_by(event_id=event_id).delete()
    db.session.commit()
    flash('Event deleted')
    print ('Event Deleted' + " " + str(event_id))
    return redirect(url_for('index'))


def parseaddr(addr):
    """
    address dict from one line format, currently only for US addresses
    i.e. 1 Washington Sq, San Jose, CA 95192
    """
    # field is None if not applicable
    street = ""
    city = ""
    state = ""
    zipcode = ""
    country = ""
    
    try:
        addr = addr.split(', ')
        street = addr[0]
        city = addr[1]
        addr = addr[2].split(' ')
        state = addr[0]
        zipcode = addr[1]
        country = 'US'
    except:
        print(":(")

    return dict(
        street=street,
        city=city,
        state=state,
        zipcode=zipcode,
        country=country,
    )


def isodate(date):
    """ convert a date in month/day/year format to year-month-day format """
    date = date.split('/')
    d = dict(
        year=date[2],
        month=date[0],
        day=date[1]
    )
    # double digit year, guess which century
    if len(d['year']) == 2:
        if int(d['year']) > 70:
            d['year'] = '19' + d['year']
        else:
            d['year'] = '20' + d['year']
    # double digit month
    if int(d['month']) < 10:
        d['month'] = '0' + d['month'][-1]
    return '-'.join([d['year'], d['month'], d['day']])
