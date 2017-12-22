from etes import app
from flask import render_template, redirect, flash, url_for, session, request
from werkzeug.utils import secure_filename
from user.form import RegisterForm, LoginForm
from event.form import SellForm
from etes import db
from event.models import Event
from user.models import User
from decimal import *
import os
import uuid
from sqlalchemy.sql import table, column, select, update, insert

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
            events = Event.query.order_by(Event.date.desc())  # For displaying based on what tickets the user is selling and displaying events by date in descending order
            # event=Event.query.all() -> for 'Upcoming Events'
            return render_template('event/home.html', event=Event.query.all())
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
   
@app.route('/confirmation')
def confirmation():
    # Who needs error checking anyways
    # if not isinstance(request.args['event_id'], int):
    #     return "Invalid event id '{}' is not a number!".format(request.args['event_id'])
    user = User.query.filter_by(username=session['username']).first().__dict__
    event = Event.query.filter_by(event_id=request.args.get('event_id')).first()
    
    name = user['fullname'].split(' ')
    user.update(dict(
        firstname=name[0],
        lastname=name[1],
        address=parseaddr(user['address']),
    ))
    
    commission = round(Decimal(event.price * Decimal(0.05)), 2)
    shipping = round(Decimal(5.00), 2)
    total = round(event.price + commission + shipping, 2)
    pricing = dict(
        commission=commission,
    return render_template('event/edit.html', form=form, event=event, action="edit")
        total=total,
    )

    return render_template('user/confirmation.html', user=user, pricing=pricing, event=event)

@app.route('/about')
def about():
    return render_template('event/about.html')
 
 
@app.route('/status')
def status():
    return "Hello World!"

@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit(event_id):
  event = Event.query.filter_by(event_id=event_id).first_or_404()
  form = SellForm(obj=event)
  if form.validate_on_submit():
    form.populate_obj(event)
    #Update form information to database
    if request.method == 'POST':
        event.name = request.form['name']
        event.
    """
    
    def editpost(id):
    post = db.session.query(Post).filter(Post.id==id).first()

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['content']

        post.title = title
        post.body = content

        db.session.commit()

        return redirect(url_for('post', id=id))
    else:
        return render_template('something.html', post=post)
    """
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('event/edit.html',form=form, event=event, action='edit')

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
    # street = ""
    # city = ""
    # state = ""
    # zipcode = ""
    # country = ""
    addr = addr.split(', ')
    street = addr[0]
    city = addr[1]
    addr = addr[2].split(' ')
    state = addr[0]
    zipcode = addr[1]
    country = 'US'
    return dict(
        street=street,
        city=city,
        state=state,
        zipcode=zipcode,
        country=country,
    )
