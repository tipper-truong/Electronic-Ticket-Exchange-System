from etes import app
from flask import render_template, redirect, url_for, session, request
from user.form import RegisterForm, LoginForm
from etes import db
from event.models import Event
from user.models import User


@app.route('/')
@app.route('/index')
def index():
  users = User.query.all()
  for user in users:
      if (user.username == session.get('username')):  # 
        events = Event.query.order_by(Event.date.desc()) #for displaying based on what tickets the user is selling and displaying events by date in descending order
        print("user: {}\nEvents(): {}".format(user.username, events))
        #event=Event.query.all() -> for 'Upcoming Events'
        return render_template('event/home.html', event=Event.query.all(), events=events)

@app.route('/login')
def logout():
  #Delete the sessions for username when the user logout
  session.pop('username', None)
  regform = RegisterForm()
  form = LoginForm()
  return render_template('user/login.html', form=form, regform=regform)

@app.route('/sell')
def sell():
   return render_template('event/sell.html', events=Event.query.all())
   
@app.route('/confirmation')
def confirmation():
   return render_template('user/confirmation.html')
   
@app.route('/about')
def about():
   return render_template('event/about.html')
 