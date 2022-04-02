from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
import models
from flask_login import login_required, current_user

timesheet = Blueprint('timesheets', __name__)



@timesheet.post('/')
# @login_required
def create_timesheet():
 
    payload = request.get_json()  
    created_timesheet = models.Timesheet.create(**payload)
    timesheet_dict = model_to_dict(created_timesheet)
    # remove the owner's password before we send it back

    return jsonify(
        data=timesheet_dict,
        message='timesheet created!',
        status=201
    ), 201

@timesheet.get('/')
def timesheet_index():

    all_timesheets = models.Timesheet.select()
    timesheet_dicts = [model_to_dict(timesheet) for timesheet in all_timesheets]
 
       
    return jsonify(
        data=timesheet_dicts,
        message=f'Fetched {len(timesheet_dicts)} timesheets!',
        status=200
    ), 200

@timesheet.get('/<id>')
def show_timesheet(id):
    try:
        
        timesheet_to_show = models.Timesheet.get_by_id(id)
        timesheet_dict = model_to_dict(timesheet_to_show)
        del timesheet_dict['owner']['password']   
        return jsonify(
            data=timesheet_dict,
            message='timesheet successfully fetched!',
            status=200
        ), 200
    except models.DoesNotExist:
      
        return jsonify(
            data={},
            message='Invalid timesheet ID',
            status=400
        ), 400

@timesheet.put('/<id>')
# @login_required
def update_timesheet(id):
    try:
        timesheet_to_update = models.Timesheet.get_by_id(id)
        # test to see if the current user is the timesheet's owner
        if timesheet_to_update.owner.id == current_user.id:
            # we need to get our payload from our request
            payload = request.get_json()
           
            timesheet_to_update.name = payload['name']
            timesheet_to_update.age = payload['age']
            timesheet_to_update.breed = payload['breed']
            timesheet_to_update.save()
            # calling save on this object will actually
            # write the changes to the database
            updated_timesheet = models.Timesheet.get_by_id(id)
            timesheet_dict = model_to_dict(updated_timesheet)
            del timesheet_dict['owner']['password']
            return jsonify(
                data=timesheet_dict,
                status=200,
                message='timesheet successfully updated'
            ), 200
        else:
            # send back an error if the wrong user is logged in
            return jsonify(
                data={},
                status=403,
                message='You do not have permission to update that timesheet'
            ), 403
    except models.DoesNotExist:
       
        return jsonify(
            data={},
            status=400,
            message='Invalid timesheet ID'
        ), 400

@timesheet.delete('/<id>')
# @login_required
def delete_timesheet(id):
    try:
        timesheet_to_delete = models.Timesheet.get_by_id(id)
        if timesheet_to_delete.owner.id == current_user.id:
            # we can use delete_instance to delete in Peewee
            timesheet_to_delete.delete_instance()
            return jsonify(
                message='timesheet successfully deleted',
                status=200
            ), 200
        else:
            return jsonify(
                message='You are not authorized to delete that timesheet',
                status=403
            ), 403
    except models.DoesNotExist:
        return jsonify(
            message='Invalid timesheet ID',
            status=400
        ), 400