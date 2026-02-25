import sqlalchemy as sa
import sqlalchemy
from components.core import database


class Visit(database.Base):
    __tablename__ = "visits"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String(10))
    caregiver_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    patient = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
