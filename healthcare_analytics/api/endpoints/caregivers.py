import fastapi

from sqlalchemy.ext import asyncio as sa_asyncio
from components.visit import (
    repository as visit_repository,
    enums as visit_enums,
    schemas as visit_schemas,
)
from components.duty import enums as duty_enums
from components.core import database

from components.user import models as user_models, enums as user_enums
from api import utils

router = fastapi.APIRouter(prefix="/caregivers", tags=["visits"])


@router.get("/progress", response_model=visit_schemas.CaregiverAnalytics)
async def get_caregiver_progress(
    current_user: user_models.User = fastapi.Depends(
        utils.require_role(
            user_enums.UserRoleEnums.CAREGIVER.value,
        )
    ),
    conn: sa_asyncio.AsyncSession = fastapi.Depends(database.get_session),
    visit_repo: visit_repository.VisitRepository = fastapi.Depends(visit_repository.VisitRepository.get),
):
    analytics = await visit_repo.get_analytics_by_caregiver(
        conn=conn,
        caregiver=current_user,
        status_visits=visit_enums.VisitStatusEnum.COMPLETED,
        status_duties=duty_enums.DutyResultStatusEnum.DONE,
    )

    return analytics
