#!/usr/bin/python3

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectField
from app.config import Config
from app.models import User, Department, Project, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Wambui:Wambui3930@localhost:3306/clockwise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'main'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app)

class UserView(ModelView):
    column_list = ('id', 'username', 'email', 'password', 'department', 'created_at')
    column_lables = {'department': 'Department'}
    form_columns = ('username', 'email', 'password', 'department_id')

    form_overrides = {
            'department': SelectField
    }
    form_args = {
            'department': {
                'widget':Select2Widget()
            }
    }

class ProjectView(ModelView):
    column_list = ('id', 'name', 'department')
    column_labels = {'department': 'Department'}
    form_columns = ('name', 'department_id')

    # Customize the form to use Select2Widget for the department field
    form_overrides = {
        'department': SelectField
    }
    form_args = {
        'department': {
            'widget': Select2Widget()
        }
    }

admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ProjectView(Project, db.session))
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
