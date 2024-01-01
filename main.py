#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectField
from app.config import Config
from app.models import User, Department, Project, Task

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash

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

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField ('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

@app.route('/', strict_slashes=False)
def home():
    return render_template('index.html')

@app.route('/tracker', strict_slashes=False)
def tracker():
    return render_template('tracker.html')

@app.route('/calendar', strict_slashes=False)
def calendar():
    return render_template('calendar.html')

@app.route('/projects_summary', strict_slashes=False)
def projects_summary():
    return render_template('projects_summary.html')

@app.route('/reports', strict_slashes=False)
def reports():
    return render_template('reports.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                department_id=1
                )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    with app.app_context():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                return redirect(url_for('tracker'))
            else:
                return render_template('login.html', form=form, error='Invalid credentials')

        return render_template('login.html', form=form)

@app.route('/save_entry', methods=['POST'])
def save_entry():
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        project_id = request.form['project']
        task_id = request.form['task']
        billable = 'billable' in request.form
        description = request.form['description']

        #need to update sqlalchemy to save data

        return redirect(url_for('success_page'))
    
    return redirect(url_for('error_page'))

@app.route('/success')
def success_page():
    return 'Form submission successful!'

@app.route('/error')
def error_page():
    return 'Error processing the form.'

if __name__ == '__main__':
    app_host = "localhost"
    app_port = 5000

    app.run(
            host=app_host,
            port=app_port,
            threaded=True
            )
