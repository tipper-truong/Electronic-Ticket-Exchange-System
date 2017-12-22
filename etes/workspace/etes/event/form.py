from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, IntegerField, DecimalField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed
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
