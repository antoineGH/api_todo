from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from todos.utils import getUserTodos, postUserTodo, getUserTodo, updateUserTodo, deleteUserTodo

todos = Blueprint('todos', __name__)

@todos.route('/api/todos', methods=['GET', 'POST'])
@jwt_required
def userTodos():
    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400
    
    if request.method == 'GET':
        return getUserTodos(user_id)

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        todo_description = content.get("todo_description", None)
        completed = content.get("completed", None)
        if not todo_description:
            return jsonify({"message": "Missing todo_description"}), 400
        return postUserTodo(todo_description, completed, user_id)

@todos.route('/api/todo/<int:todo_id>', methods=['GET', 'PUT', 'DELETE']) 
@jwt_required
def userTodo(todo_id):

    if not todo_id:
        return jsonify({"message": "Missing todo_id in request"}), 404

    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400

    if request.method == 'GET':
        return getUserTodo(todo_id, user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        todo_description = content['todo_description'] if 'todo_description' in content.keys() else ''
        completed = content['completed'] if 'completed' in content.keys() else False
        return updateUserTodo(todo_id, todo_description, completed, user_id)

    if request.method == 'DELETE':
        return deleteUserTodo(todo_id, user_id)
