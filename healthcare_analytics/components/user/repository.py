from components.core import repository
from components.user import models as user_models


class UserRepository(repository.BaseRepository):
    @staticmethod
    def get() -> "UserRepository":
        return UserRepository(model=user_models.User)
