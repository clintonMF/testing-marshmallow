from datetime import datetime
import os
from flask import Flask, request
from extension import db
from schema import CustomerSchema
from marshmallow import ValidationError
from models import Customer



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


customer_schema = CustomerSchema()
customer_login_schema = CustomerSchema(only=("username","password", "email"))
customer_schema_many = CustomerSchema(many=True)

@app.route('/')
def main():
    customers = Customer.query.all()
    return customer_schema_many.dump(customers)

@app.route('/users/<int:user_id>')
def get_user(user_id):
    customer = Customer.get_by_id(user_id)
    if not customer:
        return {"message": "user not fond"}, 404
    
    return customer_schema.dump(customer), 200
    
@app.route('/users', methods=["POST"])
def create_customer():
    try:
        json_data = request.get_json()
        try:
            data = customer_login_schema.load(json_data)
        except ValidationError as err:
            return {
                "message": "Validation error",
                "errors": err.messages
                }, 401
        email = json_data["email"]
        username = json_data["username"]
        
        
        # checking for duplicate data
        if Customer.get_by_username(username):
            return {"message": "this username exist"}, 400
        if Customer.get_by_email(email):
            return {"message": "this email exist"}, 400
        
        # unpacking the data into key word argument using **
        customer = Customer(**data)
        
        customer.save()
        
        return customer_login_schema.dump(data), 201
    except:
        return {"message": "error"}
    
if __name__ == '__main__':
    app.run(debug=True)