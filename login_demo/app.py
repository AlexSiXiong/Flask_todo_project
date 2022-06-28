from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

api = Api(app)

jwt = JWTManager(app)

@app.route('/')
def index():
    return 'Server started.'

api.add_resource(UserRegister, '/register')
api.add_resource(UserRegister, '/login')

if __name__ == '__main__':
    app.run(debug=True)

"""
curl -X POST \
http://localhost:5000/register -H \
'Content-Type: application/json' -d '{
    "username": "test",
    "password": "test"
}'
"""
