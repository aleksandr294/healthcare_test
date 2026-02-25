import sqlalchemy as sa
import sqlalchemy
from components.core import database


class DutyResult(database.Base):
    __tablename__ = "duty_results"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    duty_id = sa.Column(sa.Integer, sa.ForeignKey("duty.id"), nullable=False)
    visit_id = sa.Column(sa.Integer, sa.ForeignKey("visit.id"), nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
