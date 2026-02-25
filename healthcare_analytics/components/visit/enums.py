from enum import StrEnum


class VisitStatusEnum(StrEnum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"
    MISSED = "missed"
