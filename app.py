from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_login import LoginManager


DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.get('/')
def test_route():
    return 'App is working'

if __name__ == '__main__':
    app.run(
        port=PORT,
        debug=DEBUG
    )