from peewee import *
import datetime
from flask_login import UserMixin


DATABASE = SqliteDatabase('projects.sqlite')

class Project(Model):
    title = CharField(max_length=150)
    description = TextField(null=True)
    budget_allotment = DecimalField(max_digits=12, decimal_places=2, null=True)
    time_allotment_hours = DecimalField(max_digits=10, decimal_places=2, null=True)
    project_end_date = DateField(formats=['%Y-%m-%d'], null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    last_update = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

class User(UserMixin, Model):
    email = CharField(max_length=32, unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class TimeSheet(Model):
    project_name = CharField(max_length=150)
    project_description = TextField(null=True)
    billable = BooleanField(default=False)
    hourly_rate = DecimalField(max_digits=8, decimal_places=2, null=True)
    workday_start = DateTimeField()
    workday_end = DateTimeField()
    user = ForeignKeyField(User)
    class Meta:
        database = DATABASE
    

class UserProjectCategorizations(Model):
    user = ForeignKeyField(User)
    project = ForeignKeyField(Project)

    class Meta:
        primary_key = CompositeKey('user', 'project')
        database = DATABASE


def initialize():
    DATABASE.connect()
    # open a connection to our database
    DATABASE.create_tables([Project, User, TimeSheet, UserProjectCategorizations], safe=True)
    # the safe keyword argument means don't create the table
    # if it already exists
    # don't forget to add your models to this when you add them :)
    print('TABLES CREATED')
    DATABASE.close()
    # note in SQL we generally want to explicitly open a connection
    # and then close it when we're done