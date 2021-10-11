from flask import Flask, jsonify, abort, make_response, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, jwt_refresh_token_required, create_refresh_token, get_jwt_identity, get_jwt_claims
import datetime
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import json


# # --- INFO: LOAD CONFIG VARIABLES ---
with open('config.json') as config_file:
    config = json.load(config_file)

# --- INFO: APP CONFIGURATION ---

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DATABASE_URL')
app.config['SECRET_KEY'] =  config.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = config.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- INFO: DATABASE MODEL ---

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
    
    @property
    def serializeCompleted(self):
        if self.completed:
            return {
            'todo_id': self.todo_id,
            'todo_description': self.todo_description,
            'completed': self.completed,
        }

    @property
    def serializeNotCompleted(self):
        if not self.completed:
            return {
            'todo_id': self.todo_id,
            'todo_description': self.todo_description,
            'completed': self.completed,
        }

# --- INFO: ADMIN FUNCTIONS --- 

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
        return jsonify({"message": "Couldn't add user to DB"}), 400

def getUser(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User doesn\'t exist"}), 404
    return jsonify(user=user.serialize)

def updateUser(user_id, email, password, first_name, last_name):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": 'User doesn\'t exist'}), 404
    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if int(existing_email.user_id != int(user_id)):
                return jsonify({"message": "Email already existing"}), 404
        user.email = email
    if password:
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashedPassword
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user=user.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUser(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User doesn't exist"}), 404
    db.session.delete(user)
    try:
        db.session.commit()
        return make_response(jsonify({"message": 'Removed user with ID: {}'.format(user_id)}))
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't delete user to DB"}), 400

def getTodos():
    todos = Todo.query.all()
    return jsonify(todos=[todo.serialize for todo in todos])

def postTodo(todo_description, completed, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'No user associated'}), 400
    todo = Todo(todo_description=todo_description, completed=completed, user_id=user_id)
    db.session.add(todo)
    try:
        db.session.commit()
        return jsonify(todo=todo.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add todo to DB"}), 400

def getTodo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"message": "Todo doesn\'t exist"}), 404
    return jsonify(todo=todo.serialize)

def updateTodo(todo_id, todo_description, completed, user_id):
    user = User.query.get(user_id)
    todo = Todo.query.get(todo_id)
    if not user:
        return jsonify({'message': 'No user associated'}), 400
    if todo_description:
        todo.todo_description = todo_description
    if completed:
        todo.completed = completed
    if user_id:
        todo.user_id = user_id
    db.session.add(todo)
    try:
        db.session.commit()
        return jsonify(user=user.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteTodo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"message": "Todo doesn't exist"}), 404
    db.session.delete(todo)
    try:
        db.session.commit()
        return make_response(jsonify({"message": 'Removed todo with ID: {}'.format(todo_id)}))
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't delete todo to DB"}), 400

def getTodosUser(user_id):
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify(todos=[todo.serialize for todo in todos])

# --- INFO: AUTH FUNCTIONS --- 

def isAdmin():
    current_user = get_jwt_identity()
    print(current_user)
    return current_user == 'antoine.ratat@gmail.com'

def login(email, password):
    if not email: 
        return jsonify({"message": "Missing Email"}), 400
    if not password: 
        return jsonify({"message": "Missing Password"}), 400
    user = User.query.filter_by(email=email).first()
    if not user: 
        return jsonify({"message": "User not found"}), 404
    if user.password == '':
        return jsonify({"message": "Account not active, Set a password"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Bad email or password"}), 401
    ret = {
        'access_token': create_access_token(identity=email),
    }
    print(ret)
    return jsonify(ret), 201

def register(email, first_name, last_name, password):
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
        return jsonify({"message": "Couldn't add user to DB"}), 400

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(email=identity).first()
    return {
        'user_id' : user.user_id,
        'email': user.email,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'date_created' : user.date_created,
    }

# --- INFO: USER FUNCTIONS --- 


# --- INFO: ADMIN ROUTES ---

@app.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@app.route('/api/admin/users', methods=['GET', 'POST'])
@jwt_required
def adminUsers():
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 
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

@app.route('/api/admin/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def adminUser(user_id):
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if not user_id:
        return jsonify({"message": "Missing user_id in request"}), 404

    if request.method == 'GET':
        return getUser(user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        email = content['email'] if 'email' in content.keys() else ''
        password = content['password'] if 'password' in content.keys() else ''
        first_name = content['first_name'] if 'first_name' in content.keys() else ''
        last_name = content['last_name'] if 'last_name' in content.keys() else ''
        return updateUser(user_id, email, password, first_name, last_name)

    if request.method == 'DELETE':
        return deleteUser(user_id)

@app.route('/api/admin/todos', methods=['GET', 'POST'])
@jwt_required
def todos():
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if request.method == 'GET':
        return getTodos()
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        todo_description = content.get("todo_description", None)
        completed = content.get("completed", None)
        user_id = content.get("user_id", None)
        if not todo_description: 
            return jsonify({"message": 'Missing todo_description in JSON'})
        if not completed: 
            return jsonify({"message": 'Missing completed in JSON'})
        if not user_id: 
            return jsonify({"message": 'Missing user_id in JSON'})
        return postTodo(todo_description, completed, user_id)

@app.route('/api/admin/todo/<int:todo_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def todo(todo_id):
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if not todo_id:
        return jsonify({"message": "Missing todo_id in request"}), 404

    if request.method == 'GET':
        return getTodo(todo_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        todo_description = content['todo_description'] if 'todo_description' in content.keys() else ''
        completed = content['completed'] if 'completed' in content.keys() else ''
        user_id = content['user_id'] if 'user_id' in content.keys() else ''
        return updateUser(todo_id, todo_description, completed, user_id)

    if request.method == 'DELETE':
        return deleteTodo(todo_id)

@app.route('/api/admin/todo/user/<int:user_id>', methods=['GET'])
@jwt_required
def todosUser(user_id):
    if not isAdmin():
        return jsonify({'message': "Unauthorized Admin only"}), 403 

    if not user_id:
        return jsonify({"message": "Missing user_id in request"}), 404
    return getTodosUser(user_id)

# --- INFO: USER ROUTES ---

@app.route('/api/login', methods=['POST'])
def user_login():
    if not request.is_json: 
        return jsonify({"message": "Missing JSON in request"}), 400
    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    return login(email, password)

@app.route('/api/register', methods=['POST'])
def user_register():
    if not request.is_json: 
        return jsonify({"message": "Missing JSON in request"}), 400

    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    first_name = content.get("first_name", None)
    last_name = content.get("last_name", None)

    if not email:
        return jsonify({"message": "Missing Email"}), 400
    if not password:
        return jsonify({"message": "Missing Password"}), 400
    if not first_name:
        return jsonify({"message": "Missing First name"}), 400
    if not last_name:
        return jsonify({"message": "Missing Last name"}), 400

    return register(email, first_name, last_name, password)

if __name__ == '__main__':
    app.run(debug=True) 