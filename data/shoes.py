import sqlalchemy

from .db_session import SqlAlchemyBase


class Shoe(SqlAlchemyBase):
    __tablename__ = 'shoes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)
