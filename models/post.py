
from pymodm import EmbeddedMongoModel, MongoModel, fields
from user import User
import datetime


class Posts(MongoModel):
    author = fields.ReferenceField(User)
    added_on = fields.DateTimeField(datetime.now())
    content = fields.CharField()
    # comments = fields.EmbeddedDocumentListField(Comment)
