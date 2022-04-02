from enum import auto
from peewee import *
from flask_login import UserMixin
import datetime

# for deployment
import os
from playhouse.db_url import connect
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///work.sqlite')

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = DATABASE

class Timesheet(Model):
    project_name = CharField(max_length=150, default="React")
    notes = CharField(max_length=150)
    project_description = TextField(null=True)
    billable = BooleanField(default=False)
    hourly_rate = DecimalField(max_digits=8, decimal_places=2, null=True)
    workday_start =TimeField(default=datetime.datetime.now)
    workday_end = TimeField(default=datetime.datetime.now)
    calendar_day = DateField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)
    

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.close()  
    DATABASE.connect()

DATABASE.create_tables([User, Timesheet], safe=True)

print('TABLES CREATED')
DATABASE.close()       