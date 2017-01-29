"""SQLAlchemy database"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


class Answer(db.Model):
    id = Column(Integer, primary_key=True)
    uid = Column(String(80))
    question = Column(String(10))
    field = Column(String(80))
    value = Column(String(120))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, uid, question, field, value):
        self.uid = uid
        self.question = question
        self.field = field
        self.value = value

    def __repr__(self):
        return '<Answer {0.question}.{0.field}={0.value}>'.format(self)