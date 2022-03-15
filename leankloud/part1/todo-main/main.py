from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from d import d
from flask_cors import CORS

from resources.user import NewUser, User, UserLogin
from resources.task import NewTask, Task, UsersTask, ChageStatus

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'uvrujerajvjiqrjooijfravi' 
api = Api(app)

@app.before_first_request
def create_tables():
    d.create_all()

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401

api.add_resource(NewUser, '/create-user')
api.add_resource(User, '/user/<string:name>')
api.add_resource(UserLogin, '/login')

api.add_resource(NewTask, '/new-task')
api.add_resource(Task, '/task/<int:id>')
api.add_resource(UsersTask, '/user-tasks')
api.add_resource(ChageStatus, '/change-status/<int:id>')

d.init_app(app)

if __name__ == '__main__':
    from d import d
    d.init_app(app)
    app.run(port=8000, debug=True)