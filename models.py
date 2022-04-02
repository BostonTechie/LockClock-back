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
    notes = CharField(max_length=150)
    billable = BooleanField(default=False)
    hourly_rate = DecimalField(max_digits=8, decimal_places=2, null=True)
    workday_start =CharField(null=True)
    workday_end = CharField(null=True)
    calendar_day = CharField(null=True)
    total_bill = DecimalField(max_digits=8, decimal_places=2, null=True)
   
    
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.close()  
    DATABASE.connect()

DATABASE.create_tables([User, Timesheet], safe=True)

print('TABLES CREATED')
DATABASE.close()       