from flask import jsonify, make_response
from models import User, Todo
from __init__ import bcrypt, db
from flask_jwt_extended import get_jwt_identity

def isAdmin():
    current_user = get_jwt_identity()
    return current_user == 'antoine.ratat@gmail.com'

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
    print(user)
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
    if not todo:
        return jsonify({'message': 'No todo associated'}), 400
    if todo_description:
        todo.todo_description = todo_description
    if completed != None:
        todo.completed = completed
    if user_id:
        todo.user_id = user_id
    db.session.add(todo)
    try:
        db.session.commit()
        return jsonify(todo=todo.serialize)
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
