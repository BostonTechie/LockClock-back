from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user, current_user

import models

user = Blueprint('users', __name__)

@user.get('/')
def test_users():
    return 'User blueprint works'

@user.post('/register')
def register():
    # let's start by making sure we can get our payload
    # from our request
    payload = request.get_json()
    print(payload)
    # return 'Look at your terminal'
    # let's only create a new user if this email hasn't been used
    try:
        models.User.get(models.User.email == payload['email'])
        # in Peewee we can use .get() to retrieve a single record
        # we can use select to get them all

        return jsonify(
            data={},
            status=401,
            message='A user with that email already exists'
        ), 401
    except models.DoesNotExist:
        hashed_password = generate_password_hash(payload['password'])
        payload['password'] = hashed_password
    
        created_user = models.User.create(**payload)
        login_user(created_user)
        user_dict = model_to_dict(created_user)
        # let's delete the password before we send it back
        # it throws an error because it's not serializable
        # and we don't want to send it back anyways
        del user_dict['password']
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


@user.get('/logout')
def logout():
    logout_user()
    return jsonify(
        status=200,
        message='Successfully logged out'
    ), 200