from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
"""
    Following MVC Pattern
    Model = Database operations
    View = Templates
    Controller = views.py
"""
app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app) #making db global so we can use it everywhere

#If there's a new module, ALWAYS ADD IT HERE TO USE GLOBALLY
from event import views #get the controller from the event directory
from user import views #gets the controller from the user directory