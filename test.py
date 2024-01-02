#!/usr/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Wambui:Wambui3930@localhost:3306/clockwise'
db = SQLAlchemy(app)

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('Connection successful!')
    except Exception as e:
        print(f'Error: {e}')
