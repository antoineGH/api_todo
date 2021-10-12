import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    with app.test_request_context():
        from models import User, Todo
        db.create_all()

    from admin.routes import admin
    from users.routes import users
    from todos.routes import todos
    app.register_blueprint(admin)
    app.register_blueprint(users)
    app.register_blueprint(todos)
    return app      

    