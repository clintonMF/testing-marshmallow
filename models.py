from extension import db
from datetime import datetime

class User(db.Model):
    """ The Customer model """

    __tablename__ = "customers"

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