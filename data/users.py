import datetime
import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
import werkzeug.security

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, 
                              index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Double, default=0.0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    
    def set_password(self, password):
        self.hashed_password = werkzeug.security.generate_password_hash(password)

    def check_password(self, password):
        return werkzeug.security.check_password_hash(self.hashed_password, password)