from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
# just as a note playhouse came from installing peewee
# we use model_to_dict to translate our models into dictionaries
import models
from flask_login import login_required, current_user,  logout_user

# login_required is a function decorator
# that specify that certain routes can only be hit if we have a valid login
# current_user gives us access to the logged in user

project = Blueprint('projects', __name__)


@project.post('/')
@login_required
def create_project(id):
    payload = request.get_json()
    payload['email_id'] = current_user.id

    created_project = models.Project.create(**payload)
    project_dict = model_to_dict(created_project)
      
    return jsonify(
        data=project_dict,
        message='Project created!',
        status=201
    ), 201

@project.get('/')
@login_required
def project_index():

    all_projects = models.Project.select()
    proj_dicts = [model_to_dict(proj) for proj in all_projects]
    # for project_dict in project_dicts:
        # del project_dict['owner']['password']

    return jsonify(
        data=proj_dicts,
        message=f'Fetched {len(proj_dicts)} Projects!',
        status=200
    ), 200   

@project.get('/<id>')
@login_required
def show_project(id):
    try:
    
        project_to_show = models.Project.get_by_id(id)
        project_dict = model_to_dict(project_to_show)
        # del project_dict['owner']['password']   
        return jsonify(
            data=project_dict,
            message='project successfully fetched!',
            status=200
        ), 200
    except models.DoesNotExist:
      
        # provides error handling for our code
        return jsonify(
            data={},
            message='Invalid project ID',
            status=400
        ), 400

    