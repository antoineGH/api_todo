from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from users.utils import deleteUserUser
from users.utils import login, register, getUserUser, updateUserUser, deleteUserUser
users = Blueprint('users', __name__)

@users.route('/api/login', methods=['POST'])
def user_login():
    if not request.is_json: 
        return jsonify({"message": "Missing JSON in request"}), 400
    content = request.get_json(force=True)
    email = content.get("email", None)
    password = content.get("password", None)
    return login(email, password)

@users.route('/api/register', methods=['POST'])
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

@users.route('/api/user', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def userUser():
    claims = get_jwt_claims()
    user_id = claims.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Missing user_id in Token'}), 400

    if request.method == 'GET':
        return getUserUser(user_id)

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        content = request.get_json(force=True)
        first_name = content['first_name'] if 'first_name' in content.keys() else ''
        last_name = content['last_name'] if 'last_name' in content.keys() else ''
        password = content['password'] if 'password' in content.keys() else ''
        return updateUserUser(password, first_name, last_name, user_id)

    if request.method == 'DELETE':
        return deleteUserUser(user_id)
