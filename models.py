from peewee import *


DATABASE = SqliteDatabase('work.sqlite')

class User(Model):
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()

    DATABASE.create_tables([User], safe=True)

    print('TABLES CREATED')
    DATABASE.close()        