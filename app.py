from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
import os


DEBUG = True
PORT = 8000

app = Flask(__name__)


SESSION_SECRET = os.getenv('SESSION_SECRET')
app.secret_key = SESSION_SECRET 

@app.get('/')
def test_route():
    return 'App is working'

if __name__ == '__main__':

    print(SESSION_SECRET)
   
    app.run(
        port=PORT,
        debug=DEBUG
    )