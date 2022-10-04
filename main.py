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

@app.route('/customers/<int:customer_id>')
def get_user(customer_id):
    customer = Customer.get_by_id(customer_id)
    if not customer:
        return {"message": "user not fond"}, 404
    
    return customer_schema.dump(customer), 200
    
@app.route('/customers', methods=["POST"])
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
    
    
@app.route('/customers/<int:customer_id>', methods=["PATCH"])
def complete_registration(customer_id):
    customer = Customer.get_by_id(customer_id)
    
    if not customer:
        return {"message": "customer not found"}, 404
    
    json_data = request.get_json()
    
    try:
        data = customer_schema.load(json_data, partial=True)
    except ValidationError as err:
        return {
            "message": "Validation error",
            "errors": err.messages
            }, 401
    
    customer.username = data.get("username") or customer.username
    customer.first_name = data.get('first_name') or customer.first_name
    customer.last_name = data.get('last_name') or customer.last_name
    customer.email = data.get('email') or customer.email
    customer.phone = data.get('phone') or customer.phone
    customer.password = data.get('password') or customer.password
    customer.country = data.get('country') or customer.country
    customer.city = data.get('phone') or customer.city
    customer.state = data.get('state') or customer.state
    customer.street_name = data.get('street_name') or customer.street_name
    customer.zipcode = data.get('zipcode') or customer.zipcode
    
    customer.save()
    
    return customer_schema.dump(customer), 200
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
# data

    # "firstname": "clinton",
    # "lastname": "mekwunye",
    # "phone" : "+2348167998138",
    # "country": "Nigeria",
    # "state" : "lagos",
    # "zipcode" : 102003,
    # "city": "lagos",
    # "streetname": "commuinity road",
    # "username": "cee 22",
    # "email": "ceeeljfklj@gmail.com",
    # "password": "The gommerce app 2022"