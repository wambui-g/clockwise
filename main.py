#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db
from app.models import User, Department, Project, Task, TimeEntry
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash 


'''google calendar imports'''
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Wambui:Wambui3930@localhost:3306/clockwise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'main'
db.init_app(app)

migrate = Migrate(app, db)

admin = Admin(app, name='Admin', template_mode='bootstrap3')

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

class TaskView(ModelView):
    column_list = ('id', 'description', 'project')
    column_labels = {'project': 'Project'}
    form_columns = ('description', 'project_id')

    form_overrides = {
        'project':SelectField
    }
    form_args = {
        'project': {
            'widget': Select2Widget()
        }
    }

admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ProjectView(Project, db.session))
admin.add_view(TaskView(Task, db.session))

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])

    submit = SubmitField ('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

'''google credentials'''
def get_credentials():
    creds = None
    if "token.json" in os.listdir("."):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', strict_slashes=False)
def home():
    return render_template('index.html')

@app.route('/tracker', strict_slashes=False)
def tracker():
    projects = Project.query.all()
    tasks = Task.query.all()
    return render_template('tracker.html', projects=projects, tasks=tasks)

@app.route('/calendar', strict_slashes=False)
def calendar():
    return render_template('calendar.html')

@app.route('/calendar_new', strict_slashes=False)
def calendar_new():
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return render_template('calendar_new.html', events=[])

        return render_template('calendar_new.html', events=events)

    except HttpError as error:
        return f"An error occurred: {error}"

@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=url_for('oauth2callback', _external=True))
    session['credentials'] = 'path/to/credentials.json'  # Save credentials securely
    return redirect(url_for('calendar'))

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
                password=form.password.data,
                department_id=form.department.data
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
            email = form.email.data
            password = form.password.data

            print(f"Email: {email}, Password: {password}")

            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                login_user(user)
                print("Login successful!")
                return redirect(url_for('tracker'))
            else:
                print("Invalid credentials!")
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

        new_entry = TimeEntry(
                start_time=start_time,
                end_time=end_time,
                project_id=project_id,
                task_id=task_id,
                billable=billable,
                description=description,
                user_id=current_user.id  # Set the user_id to the current user's id
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('success_page'))
    
    return redirect(url_for('error_page'))

@app.route('/test')
def test():
    with current_app.app_context():
        try:
            projects = Project.query.all()
            print(projects)
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

        return 'Form Success'

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
