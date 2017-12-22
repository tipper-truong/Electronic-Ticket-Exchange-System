from etes import app
from flask import render_template, redirect, url_for, session, request
from user.form import RegisterForm, LoginForm
from event.form import SellForm
from etes import db
from user.models import User
import bcrypt
from address import AddressParser, Address

ap = AddressParser()
address = ap.parse_address('123 West Mifflin Street, Madison, WI, 53703')
print "Address is: {0} {1} {2} {3}".format(address.house_number, address.street_prefix, address.street, address.street_suffix)

"""
    For Register: Calling the HTTP Request (POST) to receive the forms submitted by the user and registering them to
    the database
    
    For Login: Calling the HTTP Request (GET) to receive the forms submitted by the user and see if they are a registered
    user. If they are, we log them in to the ETES Website. Else incorrect username or password
"""
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    regform = RegisterForm()
    error = None
    
    if form.validate_on_submit() or regform.validate_on_submit():
        if request.form['btn'] == 'Login':
            user = User.query.filter_by(username=form.username.data).first()
            if bcrypt.hashpw(form.password.data.encode('utf8'), user.password.encode('utf8')) == user.password.encode('utf8'): #decrypt password
                session['username'] = form.username.data
                return redirect(url_for('index'))
            else:
                error = "Incorrect username and password"
        else:
            # Check if username exists
            usernames = [u.username for u in User.query.all()]
            if regform.username.data in usernames:
                error = "username already exists!"
                print addres
                # Add user to DB
                # 574 22nd Ave San Francisco, CA 94121
                address = str(regform.house_number) + " " + regform.street + " " + regform.city + ", " + regform.state + " " + str(regform.zip_code)
                print (address)
                passwordEncrypt = bcrypt.hashpw(regform.password.data.encode('utf8'), bcrypt.gensalt()) #encrypt password
                regUser = User(
                    regform.fullname.data,
                    regform.email.data,
                    regform.username.data,
                    passwordEncrypt,
                    address)
                db.session.add(regUser)
                db.session.commit() #simulate that the record is written
                # db.session.flush()
                # error = "Registration failed!"
    return render_template('user/login.html', form=form, regform=regform, error=error)
