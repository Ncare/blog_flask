
from  datetime import datetime

from app.models import User
from app.database import db

from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer

import config

class UserService():

    @staticmethod
    def add_user(username, password, email):
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()



    @staticmethod
    def check_password(email, password):
        user = User.query.filter_by(email=email).first()
        return check_password_hash(user.password, password)


    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user and user.to_dict()

    @staticmethod
    def generate_email_token(email):
        s = TimedJSONWebSignatureSerializer(config.SECRET_KEY)
        return s.dumps({'email':email})


    @staticmethod
    def verify_email_token(token):
        s = TimedJSONWebSignatureSerializer(config.SECRET_KEY)
        try:
            email = s.loads(token)
        except:
            return False
        return email

    @staticmethod
    def update_confirmed_user(email):
        user = User.query.filter_by(email=email).first()
        user.confirmed = True
        user.confirmed_on = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        return user.to_dict()







