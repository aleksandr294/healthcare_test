import os

import dotenv
import pydantic
import pydantic_settings

dotenv.load_dotenv()


class Config(pydantic_settings.BaseSettings):
    POSTGRES_URL: pydantic.PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    model_config = pydantic.ConfigDict(env_file=".env")


config = Config()


def get_config() -> Config:
    return config
