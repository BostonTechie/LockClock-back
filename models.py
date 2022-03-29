from peewee import *
from flask_login import UserMixin


# for deployment
import os
from playhouse.db_url import connect
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///work.sqlite')



class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()
    token = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User], safe=True)

    print('TABLES CREATED')
    DATABASE.close()        