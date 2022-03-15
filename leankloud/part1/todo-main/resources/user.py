from flask_restful import Resource, reqparse
import requests
import datetime
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.user import UserModel
from models.task import TaskModal

class NewUser(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="This field is blank."
                            )
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field is blank."
                            )

        data = parser.parse_args()

        if UserModel.find_by_name(data['name']):
            return {"message": "A user with that name already exists"}, 400

        else:
            user = UserModel(data['name'])

            user.password = data['password']
            user.save_to_db()

            return {"message": "User created successfully."}, 200


class User(Resource):

    def get(self, name):
        try:
            user = UserModel.find_by_name(name)
            if not user:
                return {'message': 'User not found'}, 404
            return {'user': user.json()}, 200
        
        except:
            return {'message': 'Server Error.'}, 500

def UserTask(Resource):
    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            tasks = [task.json() for task in TaskModal.find_by_user_id(user_id)]
            return {'tasks': tasks}, 200
        except:
            return {'message': 'Server Error'}, 500

class UserLogin(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field is blank."
                                  )
        _user_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field is blank."
                                  )
        data = _user_parser.parse_args()

        user = UserModel.find_by_name(data['name'])

        if not user:
            return {'message': 'User not found.'}, 404

        if safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(
                        identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user_id': user.id,
                        "name": user.name
                    }, 200
        return {"message": "Invalid Credentials!"}, 401