from flask import Blueprint, request, Flask, g, jsonify
from flask_login import LoginManager
from flask_cors import CORS

from dotenv import load_dotenv
import os

import models

#insert the controllers the have the routes here
from resources.users import user


# set up environmental variables
DEBUG = True
PORT = 8000
app = Flask(__name__)
load_dotenv()
SESSION_SECRET = os.getenv('SESSION_SECRET')
app.secret_key = SESSION_SECRET

#handler for unauthorized requests
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def handle_unauthorized():
    # this will send back json when we make an unauthorized request
    # the default is html
    return jsonify(
        data={},
        status=401,
        message='You must be logged in to do that'
    ), 401

@login_manager.user_loader
def load_user(user_id):
    # the user_loader expects to get an id for a user
    # and it expects us to return a user if it exists
    # and None if it does not exist
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None



app.register_blueprint(user, url_prefix='/api/v1/users/')

CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000/'], supports_credentials=True)



if __name__ == '__main__':
 
    # we need to initialize our database here
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
        
    )