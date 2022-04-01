from flask import Blueprint, request, Flask, g, jsonify
from flask_login import LoginManager
from flask_cors import CORS

from dotenv import load_dotenv
import os

import models

#insert the controllers the have the routes here
from resources.users import user
from resources.timesheet import timesheet


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
app.register_blueprint(timesheet, url_prefix='/api/v1/timesheet/')

CORS(app, origins=['http://localhost:3000/', 'https://fuseclockfront2.herokuapp.com/'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000/', 'https://fuseclockfront2.herokuapp.com/'], supports_credentials=True)
CORS(timesheet, origins=['http://localhost:3000/', 'https://fuseclockfront2.herokuapp.com/'], supports_credentials=True)


@app.before_request
def before_request():
    '''Connect to the database before each request.'''
    g.db = models.DATABASE
    g.db.connect()
    # @app.before_request defines a function
    # that we want to run before EACH request

@app.after_request
def after_request(response):
    '''Close the database connection after each request.'''
    g.db.close()
    return response
    
# when something goes wrong
# the app object has an errorhandler decorator

@app.errorhandler(404)
def handle_404(err):
    return jsonify(
        data={},
        message='404: Resource not found',
        status=404
    ), 404

@app.errorhandler(405)
def handle_405(err):
    return jsonify(
        data={},
        message='405: Method not allowed',
        status=405
    ), 405

@app.errorhandler(500)
def handle_500(err):
    return jsonify(
        data={},
        message='500: Internal server error',
        status=500
    ), 500

# heroku deployment
if 'ON_HEROKU' in os.environ:
    print('\non Heroku')
    models.initialize()

if __name__ == '__main__':
    
    # we need to initialize our database here
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
        
    )