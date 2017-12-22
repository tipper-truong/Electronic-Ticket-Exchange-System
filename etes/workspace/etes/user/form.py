"""
    Responsible for Form Control for Register and Login
"""
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, IntegerField, DecimalField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed

"""
    Registering users information to the MySQL Database: etes_db
"""
class RegisterForm(Form):
    fullname = StringField('Full Name', [validators.Required(), validators.Length(min=4, max=100)])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    house_number = IntegerField('House Number', [validators.Required()])
    street = StringField('Street Address', [validators.Required()])
    city = StringField('City', [validators.Required()])
    state = StringField('State', [validators.Required()])
    zip_code = IntegerField('Zip Code', [validators.Required()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')

"""
    Successfully logging in the users after retrieving their information from MySQL Database: etes_db
"""
class LoginForm(Form):
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

"""
    A Seller Form where users input ticket data and post it to upcoming events
"""
class SellForm(Form):
    name =  StringField('Event Name', [
            validators.Required(),
            validators.Length(max=80)
        ])
    genre = StringField('Genre', [
            validators.Required(),
            validators.Length(max=80)
        ])
    venue = StringField('Venue', [
            validators.Required(),
            validators.Length(max=80)
        ])
    location = StringField('Location', [
            validators.Required(),
            validators.Length(max=80)
        ])
    date = StringField('Date', [
            validators.Required(),
            validators.Length(max=80)
        ])
    seat = StringField('Seat', [
            validators.Required(),
            validators.Length(max=80)
        ])
    starttime = StringField('Start Time', [
            validators.Required(),
            validators.Length(max=80)
        ])
    endtime = StringField('End Time', [
            validators.Required(),
            validators.Length(max=80)
        ])
    imgpath = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    
    price = DecimalField('Price',[
            validators.Required(),
        ])
    quantity = IntegerField('Quantity', [
            validators.Required(),
        ])
    