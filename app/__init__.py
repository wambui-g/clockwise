#!/usr/bin/python3
"""init file"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)

admin = Admin(app, name='Admin', template_mode='bootstrap3')
