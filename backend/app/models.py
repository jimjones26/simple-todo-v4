from backend.app import db
import bcrypt
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import re

# Define the association table
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

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

    def get_dict(self): #for returning user data
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    users = relationship("User", secondary=user_team, back_populates="teams")
    tasks = db.relationship('Task', backref='team', lazy=True)

    def __repr__(self):
        return f'<Team {self.name}>'

    def add_users(self, users):
        """Add multiple users to this team
        
        Args:
            users: List of User objects to add to the team
        """
        self.users.extend(users)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(50), default='not started')
    deadline = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def assign_user(self, user):
        """Assign a user to this task."""
        self.assignee = user

    def __repr__(self):
        return f'<Task {self.title}>'

    def update_status(self, new_status):
        """Updates the status of the task and commits to the database."""
        self.status = new_status
        db.session.commit()

def create_user(username, email, password, role):
    """Creates a new user with validation."""
    if not username or not email or not password or not role:
        raise ValueError("All fields are required")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email format")

    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")

    if User.query.filter_by(email=email).first():
        raise ValueError("Email already exists")

    user = User(username=username, email=email, role=role)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        return user
    except Exception:
        db.session.rollback()
        raise ValueError("Database error occurred")

def create_team(name, description):
    """Creates a new team."""
    if not name:
        raise ValueError("Name is required")

    if Team.query.filter_by(name=name).first():
        raise ValueError("Team name already exists")

    team = Team(name=name, description=description)

    try:
        db.session.add(team)
        db.session.commit()
        return team
    except Exception:
        db.session.rollback()
        raise ValueError("Database error occurred")

def remove_users_from_team(team_id, user_ids):
    """Removes specified users from a team
    
    Args:
        team_id: ID of the team to modify
        user_ids: List of user IDs to remove from the team
    
    Raises:
        ValueError: If team isn't found or database error occurs
    """
    team = db.session.get(Team, team_id)
    if not team:
        raise ValueError("Team not found")
    
    # Get users that exist and are in the team
    users_to_remove = [user for user in User.query.filter(User.id.in_(user_ids)) 
                      if user in team.users]
    
    # Remove users from the team
    for user in users_to_remove:
        team.users.remove(user)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Database error occurred while removing users from team")

def create_task(title, description, team_id):
    """Creates a new task."""
    if not title:
        raise ValueError("Title is required")

    if not team_id:
        raise ValueError("Team ID is required")

    team = db.session.get(Team, team_id)
    if not team:
        raise ValueError("Team not found")

    task = Task(title=title, description=description, team_id=team_id)

    try:
        db.session.add(task)
        db.session.commit()
        return task
    except Exception:
        db.session.rollback()
        raise ValueError("Database error occurred")

def update_task_deadline(task_id, new_deadline):
    """Updates the deadline of a specified task in the database.
    
    Args:
        task_id: ID of the task to update
        new_deadline: datetime object for the new deadline
        
    Returns:
        The updated Task object
        
    Raises:
        ValueError: For invalid deadlines or non-existent tasks
    """
    import datetime  # For type checking
    
    # Validate deadline type
    if not isinstance(new_deadline, datetime.datetime):
        raise ValueError("Deadline must be a valid datetime object")
    
    # Get the task
    task = db.session.get(Task, task_id)
    if not task:
        raise ValueError("Task not found")
    
    # Update and commit
    task.deadline = new_deadline
    db.session.commit()
    
    return task

def get_user_tasks(user_id):
    """Fetches all tasks assigned to a specific user.

    Args:
        user_id: The ID of the user.

    Returns:
        A list of Task objects assigned to the user.
    """
    user = db.session.get(User, user_id)
    if not user:
        return []  # Return empty list if user not found
    return Task.query.filter_by(assignee_id=user_id).all()
