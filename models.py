import datetime
from __init__ import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

class User(db.Model):
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(200), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "- USER - user_id: {}, email: {}, first_name: {}, last_name: {}, date_created: {}".format(self.user_id, self.email, self.first_name, self.last_name, self.date_created)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_created': self.date_created
        }

class Todo(db.Model):
    todo_id = Column(Integer, primary_key=True)
    todo_description = Column(String(200), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)

    def __repr__(self):
        return "- TODO - todo_id: {}, todo_description: {}, completed: {}, user_id: {}".format(self.todo_id, self.todo_description, self.completed, self.user_id)

    @property
    def serialize(self):
        return {
            'todo_id': self.todo_id,
            'todo_description': self.todo_description,
            'completed': self.completed,
        }
