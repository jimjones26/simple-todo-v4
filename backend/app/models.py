from backend.app import db
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Define the association table for the many-to-many relationship between User and Team
user_team = Table('user_team', db.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('team.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50))
    teams = relationship("Team", secondary=user_team, back_populates="users")
    tasks = db.relationship('Task', backref='assignee', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    users = relationship("User", secondary=user_team, back_populates="teams")
    tasks = db.relationship('Task', backref='team', lazy=True)

    def __repr__(self):
        return f'<Team {self.name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(50), default='not started')
    deadline = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Task {self.title}>'
