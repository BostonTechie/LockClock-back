from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user, login_required,current_user
import models
import random


user = Blueprint('users', __name__)



@user.get('/')
def get_route():
    all_users = models.User.select()
    user_dicts = [model_to_dict(user) for user in all_users]
    
    return jsonify(
    data= user_dicts,
    message=f'Fetched {len(user_dicts)} users!',
    status=200
    ), 200

@user.post('/register')
def register():

    payload = request.get_json()
    # print("🌟🌟  here i am 🌟🌟🌟",payload)

    try:
        models.User.get(models.User.email == payload['email'])
        # in Peewee we can use .get() to retrieve a single record
        return jsonify(
            data={},
            status=401,
            message='A user with that email already exists'
        ), 401
    except models.DoesNotExist:
        
        hashed_password = generate_password_hash(payload['password']) 
        payload['password'] = hashed_password
        payload['token'] = random.randint(1,10000000)
        created_user = models.User.create(**payload)
        login_user(created_user)
        user_dict = model_to_dict(created_user)
        del user_dict['password']
        print(payload)
        return jsonify(
            data=user_dict,
            message='Successfully registered',
            status=201
        ), 201

@user.post('/login')
def login():
    payload = request.get_json()
    try:
        user_to_login = models.User.get(models.User.email == payload['email'])
        # now we need to check if the password is correct
        user_dict = model_to_dict(user_to_login)
   
        # now we can check if our passwords match with check_password_hash
        valid_password = check_password_hash(user_dict['password'], payload['password'])
        # this will return true if the passwords match
        # and false if they do not
        if valid_password:
            # log the user in if the passwords match
            del user_dict['password']
            # delete the password
            
            login_user(user_to_login)
            # log in user
            return jsonify(
                data=user_dict,
                message='User logged in',
                status=200
            ), 200
        else:
            # if the passwords don't match
            # send back a vague error
            return jsonify(
                data={},
                status=401,
                message='Email or password is incorrect'
            ), 401
    except models.DoesNotExist:
        # send back a response if we get an invalid email
        return jsonify(
            data={},
            status=401,
            message='Email or password is incorrect'
        ), 401

# logout route
@user.get('/logout')
def logout():
    logout_user()
    return jsonify(
        status=200,
        message='Successfully logged out'
    ), 200

# show route
@user.get('/<id>')
def get_users(id):
    try:
        user_to_show = models.User.get_by_id(id)
        user_dict = model_to_dict(user_to_show)
      
        return jsonify(
            data=user_dict,
            message=f'Fetched {len(user_dict)} users',
            status=200
        ), 200
     
    except models.DoesNotExist:
        return jsonify(
            data=[],
            message='Invalid user ID',
            status=400
        ), 400

# edit route
