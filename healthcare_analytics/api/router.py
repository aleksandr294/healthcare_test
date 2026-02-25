import typing
import warnings

import fastapi
from fastapi.middleware import cors
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination, utils
from api.endpoints import caregivers


def configure(app: fastapi.FastAPI) -> None:
    add_pagination(app)
    warnings.simplefilter("ignore", utils.FastAPIPaginationWarning)

    router = fastapi.APIRouter(prefix="")
    router.include_router(caregivers.router)

    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def open_api() -> typing.Dict[str, typing.Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Healthcare Analytics API",
            version="v1",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = open_api

    app.include_router(router)
