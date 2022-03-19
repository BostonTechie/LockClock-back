from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user

import models

user = Blueprint('users', __name__)

@user.get('/')
def test_users():
    return 'User blueprint works'