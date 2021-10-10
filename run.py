from datetime import date, datetime
from flask import Flask, jsonify, abort, make_response, request, render_template, url_for, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from flask_cors import CORS
import json

from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean


# # --- INFO: LOAD CONFIG VARIABLES ---
with open('config.json') as config_file:
    config = json.load(config_file)

# --- INFO: APP CONFIGURATION ---

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']
app.config['SECRET_KEY'] =  config.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- INFO: DATABASE MODEL ---

class User(db.Model):
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(200), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

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

# --- INFO: REACT FUNCTIONS --- 

def getUsers():
    users = User.query.all()
    return jsonify(users=[user.serialize for user in users])

def postUser(email, password, first_name, last_name):
    userExisting = User.query.filter_by(email=email).first()
    if userExisting:
        return jsonify({'message': 'User already exists'}), 400
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashedPassword, first_name=first_name, last_name=last_name)
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user=user.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couln't add user to DB"}), 400

# --- INFO: ROUTES ---

@app.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@app.route('/api/admin/users', methods=['GET', 'POST'])
def adminUsers():
    if request.method == 'GET':
        return getUsers()
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        email = content.get("email", None)
        password = content.get("password", None)
        first_name = content.get("first_name", None)
        last_name = content.get("last_name", None)
        if not email: 
            return jsonify({"message": 'Missing email in JSON'})
        if not password: 
            return jsonify({"message": 'Missing password in JSON'})
        if not first_name: 
            return jsonify({"message": 'Missing first name in JSON'})
        if not last_name: 
            return jsonify({"message": 'Missing last name in JSON'})
        return postUser(email, password, first_name, last_name)
    

if __name__ == '__main__':
    app.run(debug=True)