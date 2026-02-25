import sqlalchemy
from components.core import database


class User(database.Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String())
    role = sqlalchemy.Column(sqlalchemy.String(20))
    full_name = sqlalchemy.Column(sqlalchemy.String(100))
    is_active = sqlalchemy.Column(sqlalchemy.Boolean)
    is_staff = sqlalchemy.Column(sqlalchemy.Boolean)
    is_superuser = sqlalchemy.Column(sqlalchemy.Boolean)
