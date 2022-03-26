from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user
import models

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
        created_user = models.User.create(**payload)
        login_user(created_user)
        user_dict = model_to_dict(created_user)
        del user_dict['password']
    
        return jsonify(
            data=user_dict,
            message='Successfully registered',
            status=201
        ), 201

# @user.post('/login')
# def login():
#     payload = request.get_json()
#     try:
#         user_to_login = models.User.get(models.User.email == payload['email'])
#         # now we need to check if the password is correct
#         user_dict = model_to_dict(user_to_login)
#         # print(user_dict)
#         # return 'look at terminal'
#         # now we can check if our passwords match with check_password_hash
#         valid_password = check_password_hash(user_dict['password'], payload['password'])
#         # this will return true if the passwords match
#         # and false if they do not
#         if valid_password:
#             # log the user in if the passwords match
#             del user_dict['password']
#             # delete the password
#             # remember we can't send back anyway
#             login_user(user_to_login)
#             # log in user
#             return jsonify(
#                 data=user_dict,
#                 message='User logged in',
#                 status=200
#             ), 200
#         else:
#             # if the passwords don't match
#             # send back a vague error
#             return jsonify(
#                 data={},
#                 status=401,
#                 message='Email or password is incorrect'
#             ), 401
#     except models.DoesNotExist:
#         # send back a response if we get an invalid email
#         return jsonify(
#             data={},
#             status=401,
#             message='Email or password is incorrect'
#         ), 401
#         # some say you should vague like this
#         # others disagree

@user.get('/logout')
def logout():
    logout_user()
    return jsonify(
        status=200,
        message='Successfully logged out'
    ), 200

# @user.get('/<id>/dogs')
# def get_users_dogs(id):
#     try:
#         # get all dogs that a particular user owns
#         # first way:
#         # dog_user = models.User.get_by_id(id)
#         # dog_dicts = [model_to_dict(dog) for dog in dog_user.dogs]
#         # for dog_dict in dog_dicts:
#         #     del dog_dict['owner']
#         # return jsonify(
#         #     data=dog_dicts,
#         #     message=f'Fetched {len(dog_dicts)} dogs',
#         #     status=200
#         # ), 200
#         # second way
#         dogs = (models.Dog
#             .select(
#                 models.Dog.id,
#                 models.Dog.name,
#                 models.Dog.breed,
#                 models.Dog.age,
#                 models.Dog.created_at
#             )
#             .where(models.Dog.owner == id)
#             .dicts())
#         dogs = list(dogs)
#         return jsonify(
#             data=dogs,
#             message=f'Fetched {len(dogs)} dogs',
#             status=200
#         ), 200
#     except models.DoesNotExist:
#         return jsonify(
#             data=[],
#             message='Invalid user ID',
#             status=400
#         ), 400