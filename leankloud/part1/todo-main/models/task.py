from d import db
import datetime
import requests

class TaskModal(d.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    task = db.Column(db.String())
    dueDate = db.Column(db.Date)
    status = db.Column(db.String(), default = "Not started")
    createdOn = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self,user_id, task, dueDate):
        self.user_id = user_id
        self.task = task
        self.dueDate = dueDate
        # self.status = status

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'task': self.task,
            'status': self.status,
            'createdOn': str(self.createdOn),
            'dueDate': str(self.dueDate)
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_id_user_id(cls, id, user_id):
        return cls.query.filter_by(id=id, user_id=user_id).first()