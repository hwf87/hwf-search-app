from pydantic import BaseSettings


class AppSettings(BaseSettings):
    APP_NAME: str = "HWF SEARCH API"
    PRE_TRAIN_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    ES_HOST: str
    ES_USERNAME: str
    ES_PASSWORD: str
    ES_ALIAS: str

    class Config:
        env_file = ".env"


class SearchSettings(AppSettings):
    SERCH_FIELDS: list = []
    AGGREGATION_FIELDS: list = []
    HIGHLIGHT_FIELDS: list = []


settings = SearchSettings()
