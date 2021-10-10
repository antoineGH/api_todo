from flask import Flask, jsonify, abort, make_response, request, render_template, url_for, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from flask_cors import CORS
import json


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

# --- INFO: REACT FUNCTIONS --- 

# --- INFO: ROUTES ---

@app.route('/')
def home():
    return render_template('documentation.html', title='Documentation')


if __name__ == '__main__':
    app.run(debug=True)