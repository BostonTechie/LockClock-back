from flask import Blueprint, request, Flask, g, jsonify
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS
from flask_login import login_user, logout_user

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

@app.get('/')
def test_route():
    return 'App is working'

@app.get('/get')
def get_route():
    all_users = models.User.select()
    user_dicts = [model_to_dict(user) for user in all_users]
    
    return jsonify(
    data= user_dicts,
    message=f'Fetched {len(user_dicts)} users!',
    status=200
    ), 200

@app.post('/register')
def register():

    payload = request.get_json()
    print(payload)

    try:
        models.User.get(models.User.email == payload['email'])
        # in Peewee we can use .get() to retrieve a single record
        return jsonify(
            data={},
            status=401,
            message='A user with that email already exists'
        ), 401
    except models.DoesNotExist:
        print(payload)
        # return "Look at terminal"
        created_user = models.User.create(**payload)
       
        user_dict = model_to_dict(created_user)
        # let's delete the password before we send it back
        # it throws an error because it's not serializable
        # and we don't want to send it back anyways
  
        return jsonify(
            data=user_dict,
            message='Successfully registered',
            status=201
        ), 201

if __name__ == '__main__':
    # print('Session Secret:', SESSION_SECRET)
    # we need to initialize our database here
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
    )