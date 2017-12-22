from etes import app
from flask import render_template, redirect, flash, url_for, session, request, abort
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
import datetime
import math


# Global vars/settings

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TICKET_WINDOW = 60*2


"""
    Using an HTTP Request (GET) to...
    Display the events under "Upcoming Events"
    Display what tickets the user are current selling under "My Listing" 
    Display what tickets the user bought under "Bought Tickets"
"""
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
        # User is signed in
        if session.get('username') in usernames:
            user = User.query.filter_by(username=session['username']).first()
            event = Event.query.filter(Event.quantity > 0).all()  # Don't get sold o

            # ticket race condition while we're at it
            for ev in event:
                totalqty = ev.quantity
                pendingtickets = Ticket.query.filter_by(event_id=ev.event_id, bought=0).all()
                for t in pendingtickets:
                    # Count pending tickets if within time window
                    expiry = datetime.datetime.now() - datetime.timedelta(seconds=TICKET_WINDOW)
                    tickettime = datetime.datetime.strptime(t.timestamp, TIME_FORMAT)
                    if tickettime > expiry:
                        print("ticket #{} expires on {}".format(t.ticket_id, expiry))
                        totalqty -= 1
                    else:
                        # print('ticket #{} has expired'.format(t.ticket_id))
                        pass
                # print('ev: {}, total: {}'.format(ev.quantity, totalqty))
                ev.quantity = totalqty

            # Order date by ascending
            for ev in event:
                # sorting
                print(ev.date)
                usformat_date = re.findall('[0-9/]+', ev.date)  # REGEX MAGIC LOL
                if len(usformat_date) > 0:
                    dateparse = isodate(usformat_date[0])
                else:
                    dateparse = ''
                ev.isodate = dateparse
            event = sorted(event, key=lambda o: o.isodate)
            # Filter out events that ended
            today = datetime.date.today().isoformat()
            upcoming = [ev for ev in event if ev.isodate >= today]
            myevents = [ev for ev in event if ev.user_id == user.id]

            return render_template('event/home.html', upcoming=upcoming, myevents=myevents, tickets=Ticket.query.all(), user=user)
        # Redirect to login
        else:
            return """
            <meta http-equiv="refresh" content="5;url=/login" />
            <p>Please log first. You'll be redirected in 5 seconds, or click <a href="/login">here</a>!</p>
            """


"""
    After the user logged out, the session['username'] is destroyed
"""
@app.route('/login')
def logout():
  #Delete the sessions for username when the user logout
  session.pop('username', None)
  regform = RegisterForm()
  form = LoginForm()
  return render_template('user/login.html', form=form, regform=regform)


"""
    Calling the HTTP Request (POST) from the form the user submit and adding their ticket information they want to 
    sell to the database
"""
@app.route('/sell', methods=('GET', 'POST'))
def sell():
    form = SellForm()
    if form.validate_on_submit():
        #Save image to static/images
        app.config['UPLOAD_FOLDER'] = 'static/images'
        file = request.files.get('imgpath')
        # image uploaded
        if file.__bool__():
            print("uploaded file")
            extension = os.path.splitext(file.filename)[1]
            f_name = str(uuid.uuid4()) + extension  #encoding the image name + adding extension like jpg, png etc.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))  #saving the image to static/images
        # No image
        else:
            print("use placeholder")
            f_name = "Background.png"
        event = Event(
            form.name.data,
            form.genre.data,
            form.venue.data,
            form.location.data,
            form.date.data,
            form.starttime.data,
            form.endtime.data,
            "static/images/" + f_name,
            User.query.filter_by(username=session['username']).first(),
            form.price.data,
            form.quantity.data
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event/sell.html', form=form)


"""
    Calling the HTTP Request (POST) to add their payment information to the database and give the bought ticket to the new owner
    Calling the HTTP Request (GET) to retrieve the user information and displaying it on the forms so they don't have to re-type
    @param: event_id -> The ticket they want to buy
"""
@app.route('/confirmation/<int:event_id>', methods=['POST', 'GET'])
def confirmation(event_id):
    event = Event.query.filter_by(event_id=event_id).first()
    user = User.query.filter_by(username=session['username']).first()
    print(request.method + " REQUEST_METHOD")

    # Event doesn't exist
    if event is None:
        return abort(404)
    # Can't access sold out events
    if event.quantity == 0:
        return redirect(url_for('index'))
    # User can't buy their own event
    seller = User.query.filter_by(id=event.user_id).first()
    if session['username'] == seller.username:
        return """
        <meta http-equiv="refresh" content="5;url=/" />
        <p>Sorry, you can't buy your own event! Were you trying to buy something else? You'll be redirected back home in 5 seconds, or click <a href="/">here</a>!</p>
        """

    if request.method == 'GET':
        # Get user and event details
        # event = Event.query.filter_by(event_id=event_id).first()
        user = User.query.filter_by(username=session['username']).first().__dict__
        # Make things easier and pre process/parse user info
        user.update(parsename(user['fullname']))
        user.update(parseaddr(user['address']))
        # gimme yer monies
        commission = round(Decimal(event.price * Decimal(0.05)), 2)
        shipping = round(Decimal(5.00), 2)
        total = round(event.price + commission + shipping, 2)
        pricing = dict(
            commission=commission,
            shipping=shipping,
            total=total,
        )
        # Dummy ticket to hold your place
        ticket = Ticket(
            event.event_id,
            None,
            user['id'],
            0,  # bought
            user['firstname'],
            user['lastname'],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            datetime.datetime.now().strftime(TIME_FORMAT)  # timestamp
        )
        #db.session.add(ticket)
        #db.session.commit()

        return render_template('user/confirmation.html', user=user, pricing=pricing, event=event)
    if request.method == 'POST':
        # verify form
        # insert into tickets
        # redirect to order /status/event_id
        ticket = Ticket(
            event.event_id,
            event.user_id,
            user.id,
            1, # bought
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
            request.form['cvv'],
            datetime.datetime.now().strftime(TIME_FORMAT) # timestamp
        )
        db.session.add(ticket)
        event.quantity -= 1 #decrement quantity
        db.session.commit()
        return redirect(url_for('status', event_id=event_id))
    print("How did I get here")
    return render_template('user/confirmation2.html')


"""
    Displays the About Page of the ETES Website Team
"""
@app.route('/about')
def about():
    return render_template('event/about.html')


"""
    Calculating the distance between the seller and the buyer 
    Decrease the quantity of the ticket after it's bought and update it to the database
"""
@app.route('/status/<int:event_id>',  methods=['GET', 'POST'])
def status(event_id):
    # Get info about ticket, user, event, etc.
    usr = User.query.filter_by(username=session['username']).first()
    event = Event.query.filter_by(event_id=event_id).first()
    buyeraddr = usr.address
    selleraddr = event.user.address #gets the seller address
    print ("Buyer:{}\nSeller:{}".format(buyeraddr, selleraddr))
    
    # Calculate the distance between buyeraddr and selleraddr
    distance = 0
    geolocator = GoogleV3()
    print (buyeraddr + " buyer address")
    print (selleraddr + " seller address")
    
    buyerlocation = geolocator.geocode(buyeraddr)
    sellerlocation = geolocator.geocode(selleraddr)

 
    buyer_lat_lon = (buyerlocation.latitude, buyerlocation.longitude)
    seller_lat_lon = (sellerlocation.latitude, sellerlocation.longitude)
    distance = vincenty(buyer_lat_lon, seller_lat_lon).miles
    distance = round(distance, 2)  # shorten distsance output
    
    if (request.method == 'GET'):
        pass
    if (request.method == 'POST'):
        pass

    return render_template('user/status.html', usr=usr, selleraddr=selleraddr, buyeraddr=buyeraddr, distance=distance)


"""
    Calling HTTP Request (POST) after user re-edits their selling ticket. Once the information is updated, it is updated to the database
    @param: event_id -> The ticket they want to edit and update in the "Upcoming Event" 
"""
@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit(event_id):
    event = Event.query.filter_by(event_id=event_id).first_or_404()
    user = User.query.filter_by(id=event.user_id, username=session['username']).first_or_404() # only access their own events

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
        else:
            event.imgpath = original_image
        # Commit changes to event and return to homepage
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event/edit.html', form=form, event=event, action="edit")


"""
    Deletes the selling ticket from the database. 
    @param: event_id -> The ticket to delete
"""
@app.route('/delete/<int:event_id>', methods=['GET', 'POST'])
def delete(event_id):
    # Check if event exists, and user owns it
    event = Event.query.filter_by(event_id=event_id).first_or_404()
    user = User.query.filter_by(id=event.user_id, username=session['username']).first_or_404()
    
    event = Event.query.filter_by(event_id=event_id)
    e
    
    db.session.commit()
    flash('Event deleted')
    print ('Event Deleted' + " " + str(event_id))
    return redirect(url_for('index'))


"""
    Parsing the address information from the user
"""
def parseaddr(addr):
    """
    Address dict from one line format, currently only for US addresses
    i.e. 1 Washington Sq, San Jose, CA 95192
    """
    # field is None if not applicable
    street = ""
    city = ""
    state = ""
    zipcode = ""
    country = ""
    try:
        firstaddr = addr.split(', ')
        street = firstaddr[0]
        city = firstaddr[1]
        secondaddr = firstaddr[2].split(' ')
        state = secondaddr[0]
        zipcode = re.search('[0-9]{5}', addr).group(0)
        country = 'US'
    except Exception as e:
        print('parseaddr() hit an exception :(')
        print(e)
    return dict(
        street=street,
        city=city,
        state=state,
        zipcode=zipcode,
        country=country,
    )

"""
    A helper function to display the events in descending order by date that reads the date of the event and modifies it.
    @date -> The date to modify and order
"""
def isodate(date):
    """ Convert a date in month/day/year format to iso year-month-day format """
    date = date.split('/')
    d = dict(
        year=date[2],
        month=date[0],
        day=date[1]
    )
    # Double digit year, guess which century
    if len(d['year']) == 2:
        # Sorta unix time, if after XX70 then it's the 1900s
        if int(d['year']) > 70:
            d['year'] = '19' + d['year']
        else:
            d['year'] = '20' + d['year']
    # Single digit month
    if int(d['month']) < 10:
        d['month'] = '0' + d['month'][-1]
    # Single digit date
    # lol no need
    return '-'.join([d['year'], d['month'], d['day']])
    

"""
    Helper function to parse user entered name into first and last name
    @fullname -> the full name that user registered with, can be one word or multi word
"""
def parsename(fullname):
    fullname = fullname.split(' ')
    name = dict(
        firstname=fullname[0],
        lastname=''
    )
    if len(fullname) > 1:
        name.update(dict(lastname=fullname[1:]))
    return name