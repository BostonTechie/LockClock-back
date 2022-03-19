from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
# just as a note playhouse came from installing peewee
# we use model_to_dict to translate our models into dictionaries
import models
from flask_login import login_required, current_user

# login_required is a function decorator
# that specify that certain routes can only be hit if we have a valid login
# current_user gives us access to the logged in user

project = Blueprint('projects', __name__)


@project.get('/')
def test_users():
    return 'project blueprint works'