from pydantic import Field

from pydantic_settings import BaseSettings


class ETLSettings(BaseSettings):
    LOGGING_LEVEL: str = Field(env="LOGGING_LEVEL")
    FILEMODE: str = Field(env="FILEMODE")
    FILENAME: str = Field(env="FILENAME")
    ORGANIZATION_NAME: str = Field(env="ORGANIZATION_NAME")
    API_URL: str = Field(env="API_URL")
    ACCESS_TOKEN: str = Field(env="ACCESS_TOKEN")
    FILE_PATH: str = Field(env="FILE_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


etl_settings = ETLSettings()
