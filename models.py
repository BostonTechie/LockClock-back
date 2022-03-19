from peewee import *
import datetime
from flask_login import UserMixin


# DATABASE = SqliteDatabase('dogs.sqlite')

class Project(Model):
    title = CharField(max_length=150)
    description = TextField(null=True)
    budget_allotment = DecimalField(max_digits=12, decimal_places=2, null=True)
    time_allotment_hours = DecimalField(max_digits=10, decimal_places=2, null=True)
    project_end_date = DateField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    last_update = DateTimeField(auto_now=True)

class TimeSheet(Model):
    project_name = CharField(max_length=150)
    project_description = TextField(null=True)
    billable = BooleanField()
    hourly_rate = DecimalField(max_digits=8, decimal_places=2, null=True)
    workday_start = DateTimeField()
    workday_end = DateTimeField()

class User(Model):
    user = CharField(max_length=32)
    email = CharField(max_length=32, unique=True)

class UserProjectCategorizations(Model):
    user = ForeignKeyField(User)
    project = ForeignKeyField(Project)

    class Meta:
        primary_key = CompositeKey('user', 'project')