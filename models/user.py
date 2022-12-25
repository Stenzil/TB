from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from DAL import Database


class Users(MongoModel):

    emailID = fields.EmailField(primary_key=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    YOB = fields.CharField(required=True)
    password = fields.CharField(required=True)

    @staticmethod
    def AddUser(u):
        Database.initialize()
        print('ssssssssssssssssssssss')
        print(type(u))
        print(u.first_name)
        Database.insert('users', u)
