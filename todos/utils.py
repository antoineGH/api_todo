from flask import jsonify, make_response
from models import Todo, User
from __init__ import db

def getUserTodos(user_id):
    todos = Todo.query.filter_by(user_id=user_id).all()
    if not todos: 
        return jsonify({"message": "Todos not found"}), 404
    return jsonify(todos=[todo.serialize for todo in todos])

def postUserTodo(todo_description, completed, user_id):
    todo = Todo(todo_description=todo_description, completed=completed, user_id=user_id)
    db.session.add(todo)
    try:
        db.session.commit()
        return jsonify(todo=todo.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add todo to DB"}), 400

def getUserTodo(todo_id, user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"message": "User not found"}), 404
    todo = Todo.query.get(todo_id)
    if not todo: 
        return jsonify({"message": "Todo not found"}), 404
    if todo.user_id != user.user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    return jsonify(todo=todo.serialize)

def updateUserTodo(todo_id, todo_description, completed, user_id):
    todo = Todo.query.get(todo_id)
    if not todo: 
        return jsonify({"message": "Todo not found"}), 404
    if todo.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    if todo_description:
        todo.todo_description = todo_description
    if completed != None:
        todo.completed = completed
    db.session.add(todo)
    try:
        db.session.commit()
        return jsonify(todo=todo.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUserTodo(todo_id, user_id):
    todo = Todo.query.get(todo_id)
    if not todo: 
        return jsonify({"message": "Todo not found"}), 404
    if todo.user_id != user_id:
        return jsonify({"message": "Unauthorized Access"}), 401
    db.session.delete(todo)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)
