#!/usr/bin/python3

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.config import Config
from app.models import User, Department, Project, Task

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Task, db.session))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app_host = "localhost"
    app_port = 5000

    app.run(
            host=app_host,
            port=app_port,
            threaded=True
            )
