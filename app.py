from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
import os

import models
# import my various controllers where my routes are
from resources.controllers.users import user


DEBUG = True
PORT = 8000

app = Flask(__name__)

SESSION_SECRET = os.getenv('SESSION_SECRET')
app.secret_key = SESSION_SECRET 


app.register_blueprint(user, url_prefix='/api/v1/users')


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

# let's set up some error handlers to send back JSON
# when something goes wrong
# the app object has an errorhandler decorator


@app.get('/')
def test_route():
    return 'App is working'

if __name__ == '__main__':

    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
    )