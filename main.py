from datetime import datetime
import os
from flask import Flask, request
from extension import db
from schema import UserSchema
from marshmallow import ValidationError
from models import User



app = Flask(__name__)
       
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()

user_login_schema = UserSchema(only=("username","password", "email"))
user_schema_many = UserSchema(many=True)

@app.route('/')
def main():
    users = User.query.all()
    return user_schema_many.dump(users)

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.get_by_id(user_id)
    
    return UserSchema().dump(user), 200
    
@app.route('/users', methods=["POST"])
def create_user():
    try:
        json_data = request.get_json()
        try:
            data = user_login_schema.load(json_data)
        except ValidationError as err:
            return {
                "message": "Validation error",
                "errors": err.messages
                }, 401
        user = User(**data)
        
        user.save()
        return user_login_schema.dump(data), 201
    except:
        return {"message": "error"}
    
if __name__ == '__main__':
    app.run(debug=True)