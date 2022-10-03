from marshmallow import Schema, fields, ValidationError,  validate
from passlib.hash import pbkdf2_sha256

def password_strength(s):
    l, u, p, d = 0, 0, 0, 0
    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_ %&#-=+;:?{}~\/"
    digits="0123456789"
    if (len(s) >= 8):
        for i in s:
            
            # counting lowercase alphabets
            if (i in smallalphabets):
                l+=1		

            # counting uppercase alphabets
            if (i in capitalalphabets):
                u+=1		

            # counting digits
            if (i in digits):
                d+=1		

            # counting the mentioned special characters
            if(i in specialchar):
                p+=1
    if (l>=1 and u>=1 and p>=1 and d>=1):
        print("Valid Password")
        return True
    else:
        print("Invalid Password")
        raise ValidationError("password is very weak")

class UserSchema(Schema):
    class Meta: ordered = True
    
    id = fields.Int(dump_only = True)
    firstname = fields.String(validate=[validate.Length(max=100, min=2)])
    lastname = fields.String(validate=[validate.Length(max=100, min=2)])
    phone = fields.String(validate=[validate.Length(max=15, min=2)])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    country = fields.String(validate=[validate.Length(max=100, min=2)])
    state = fields.String(validate=[validate.Length(max=100, min=2)])
    zipcode = fields.Integer()
    city = fields.String(validate=[validate.Length(max=100)])
    street_name = fields.String(validate=[validate.Length(max=100, min=2)])
    username = fields.String(required=True, validate=[validate.Length(max=100)])
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')
    
    def load_password(self, password):
        if password_strength(password) == True:
            return pbkdf2_sha256.hash(password)