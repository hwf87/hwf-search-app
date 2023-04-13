from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "HWF SEARCH API"
    ES_HOST: str
    ES_USERNAME: str 
    ES_PASSWORD: str
    ES_ALIAS: str

    class Config:
        env_file = ".env"

settings = Settings()