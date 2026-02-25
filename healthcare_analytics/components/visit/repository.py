from components.core import repository
from components.visit import models as visit_models, enums as visit_enums

import sqlalchemy as sa
from components.duty import models as duty_models, enums as duty_enums
from components.user import models as user_models
from sqlalchemy.ext import asyncio as sa_asyncio


class VisitRepository(repository.BaseRepository):
    @staticmethod
    def get() -> "VisitRepository":
        return VisitRepository(model=visit_models.Visit)

    async def get_analytics_by_caregiver(
        self,
        conn: sa_asyncio.AsyncSession,
        caregiver: user_models.User,
        status_visits: visit_enums.VisitStatusEnum,
        status_duties: duty_enums.DutyResultStatusEnum,
    ) -> dict:
        query = (
            sa.select(
                sa.func.count(sa.distinct(visit_models.Visit.id)).label("visit_count"),
                sa.func.count(sa.distinct(duty_models.DutyResult.id)).label("duty_count"),
            )
            .select_from(visit_models.Visit)
            .outerjoin(
                duty_models.DutyResult,
                sa.and_(
                    visit_models.Visit.id == duty_models.DutyResult.visit_id,
                    duty_models.DutyResult.status != status_duties.value,
                ),
            )
            .where(
                visit_models.Visit.caregiver_id == caregiver.id,
                visit_models.Visit.status != status_visits.value,
            )
        )
        result = await conn.execute(query)
        row = result.mappings().first()
        return dict(row) if row else {"visit_count": 0, "duty_count": 0}
