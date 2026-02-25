from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from components.core import config
from sqlalchemy.ext import asyncio as sa_asyncio
from components.core import database
from components.user import repository as user_repository, models as user_models

cng = config.get_config()
security = HTTPBearer()


async def get_current_user(
    token: str = Depends(security),
    conn: sa_asyncio.AsyncSession = Depends(database.get_session),
    user_repo: user_repository.UserRepository = Depends(user_repository.UserRepository.get),
):
    try:
        payload = jwt.decode(token.credentials, cng.SECRET_KEY, algorithms=[cng.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID missing in token",
            )

        user = await user_repo.get_by_id(id=int(user_id), conn=conn)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

        return user

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def require_role(*allowed_roles: str):
    def _require_role(current_user: user_models.User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role. Allowed roles: {allowed_roles}",
            )
        return current_user

    return _require_role
