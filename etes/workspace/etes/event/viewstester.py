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


event = Event.query.all()

# Order date by descending
# print([re.search('(([0-9]+/?)+)',date).group(0).split('/') for date in event])


#events = Event.query.order_by(Event.date.desc())  # For displaying based on what tickets the user is selling and displaying events by date in descending order



user = User.query.filter_by(username=session['username']).first()
