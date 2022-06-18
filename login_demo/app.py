from flask import Flask
from flask_restful import Api

from user import UserRegister

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

@app.route('/')
def index():
    return 'Server started.'

api.add_resource(UserRegister, '/register')

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
