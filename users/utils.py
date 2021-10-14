from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from models import User
from __init__ import db, bcrypt, jwt

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
    }

def getUserUser(user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"message": "User not found"}), 404
    return jsonify(user=user.serialize)

def updateUserUser(password, first_name, last_name, user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"message": "User not found"}), 404
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user=user.serialize)
    except:
        db.session.rollback()
        return jsonify({"message": "Couldn't add user to DB"})

def deleteUserUser(user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    try:
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)

