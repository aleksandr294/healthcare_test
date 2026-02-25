import pydantic


class CaregiverAnalytics(pydantic.BaseModel):
    visit_count: int
    duty_count: int
