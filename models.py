from peewee import *
from flask_login import UserMixin


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
    project_name = CharField(max_length=150)
    notes = CharField(max_length=150)
    project_description = TextField(null=True)
    billable = BooleanField()
    hourly_rate = DecimalField(max_digits=8, decimal_places=2, null=True)
    workday_start =TimeField()
    workday_end = TimeField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()

DATABASE.create_tables([User, Timesheet], safe=True)

print('TABLES CREATED')
DATABASE.close()        