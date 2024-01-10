#!/usr/bin/python3
"""module to define database models"""

from datetime import datetime
from app import db
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    created_at =db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.created_at}')"


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    """define relationship with user"""
    users = db.relationship('User', backref='department', lazy=True)

    """define relationship with project"""
    projects = db.relationship('Project', backref='department', lazy=True)

    def __repr__(self):
        return f"Department('{self.name}')"


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    """relationship with Task Model"""
    tasks = db.relationship('Task', backref='project', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}')"


class Task(db.Model):
    __tablename__ = 'task'
    id  = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.description}')"

class TimeEntry(db.Model):
    __tablename__ = 'time_entry'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    billable = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"TimeEntry('{self.start_time}', '{self.end_time}', '{self.project_id}', '{self.task_id}', '{self.billable}', '{self.description}', '{self.user_id}')"
