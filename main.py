from datetime import datetime
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from schema import UserSchema
from marshmallow import ValidationError



app = Flask(__name__)
       
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    """ The Customer model """

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(32), nullable=False, unique=True)
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15))
    password = db.Column(db.Text(), nullable=False)
    country = db.Column(db.String(50))
    state = db.Column(db.String(70))
    city = db.Column(db.String(50))
    street_name = db.Column(db.String(50))
    zipcode = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()


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
    db.create_all()
    app.run(debug=True)