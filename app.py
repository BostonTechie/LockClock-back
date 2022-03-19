from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
import os

import models
# import my various controllers where my routes are
from resources.controllers.users import user
from resources.controllers.projects import project


DEBUG = True
PORT = 8000 

app = Flask(__name__)
 
load_dotenv()

SESSION_SECRET = os.getenv('SESSION_SECRET')
app.secret_key = SESSION_SECRET 

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


app.register_blueprint(user, url_prefix='/api/v1/users')
app.register_blueprint(project, url_prefix='/api/v1/projects')


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(project, origins=['http://localhost:3000'], supports_credentials=True)


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None
    

@app.before_request
def before_request():
    '''Connect to the database before each request.'''
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    '''Close the database connection after each request.'''
    g.db.close()
    return response


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



@app.get('/')
def test_route():
    return 'App is working'

if __name__ == '__main__':
    
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
    )