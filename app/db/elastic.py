from elasticsearch import Elasticsearch
from config import settings


def get_es_client() -> Elasticsearch:
    """ """
    client = Elasticsearch(
        settings.ES_HOST,
        http_auth = (
            settings.ES_USERNAME, settings.ES_PASSWORD
        ),
        verify_certs = False,
        timeout = 30,
        max_retries = 10,
        retry_on_timeout = True
    )
    return client