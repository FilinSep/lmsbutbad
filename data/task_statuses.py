import sqlalchemy
from .db_session import SqlAlchemyBase


class TaskStatuses(SqlAlchemyBase):
    __tablename__ = 'task_statuses'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    task = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String, default='CHECK')
