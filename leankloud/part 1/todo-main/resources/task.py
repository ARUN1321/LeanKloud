from flask_restful import Resource, reqparse
import requests
import datetime
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.task import TaskModal

class NewTask(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('task',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('dueDate',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        try:
            data = parser.parse_args()

            data['user_id'] = get_jwt_identity()

            dueDate = datetime.datetime.strptime(data['dueDate'], '%Y-%m-%d')

            task = TaskModal(data['user_id'], data['task'], dueDate)

            task.save_to_db()

            return {'message': 'Task added successfuly', 'task': task.json()}, 200

        except:
            return {'message': 'Internal Server Error'}, 500

class Task(Resource):

    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            task = TaskModal.find_by_id_user_id(id, user_id)
            if not task:
                return {'message': 'Task not found!'}, 404
            return {"task": task.json()}, 200
        except:
            return {'message': 'Internal Server Error'}, 500
 
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()

        parser.add_argument('task',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('dueDate',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        try:
            data = parser.parse_args()
            user_id = get_jwt_identity()
            task = TaskModal.find_by_id_user_id(id, user_id)
            if not task:
                return {'message': 'Task not found!'}, 404
                
            task.task = data['task']
            dueDate = datetime.datetime.strptime(data['dueDate'], '%Y-%m-%d')
            task.dueDate = dueDate
            
            task.save_to_db()
            return {"task": task.json()}, 200
        except:
            return {'message': 'Internal Server Error'}, 500

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            task = TaskModal.find_by_id_user_id(id, user_id)
            if not task:
                return {'message': 'Task not found!'}, 404
            task.delete_from_db()
            return {"message": "Deleted"}, 200
        except:
            return {'message': 'Internal Server Error'}, 500

class ChageStatus(Resource):
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        
        parser.add_argument('status',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        try:
            data = parser.parse_args()
            user_id = get_jwt_identity()
            task = TaskModal.find_by_id_user_id(id, user_id)
            if not task:
                return {'message': 'Task not found!'}, 404
            task.status = data['status']
            task.save_to_db()
            return {"task": task.json()}, 200
        except:
            return {'message': 'Internal Server Error'}, 500


class UsersTask(Resource):

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            tasks = [task.json() for task in TaskModal.find_by_user_id(user_id)]
            return {'tasks': tasks}, 200
        except:
            return {'message': 'Internal Sever Error'}, 500

 