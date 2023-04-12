from elasticsearch import Elasticsearch

def get_es_client() -> Elasticsearch:
    host = "http://127.0.0.1:9200"
    elasticsearch_username = "elastic"
    elasticsearch_password = "elastic"
    client = Elasticsearch(
        host,
        http_auth=(elasticsearch_username, elasticsearch_password),
        verify_certs=False,
        timeout=30,
        max_retries=10,
        retry_on_timeout=True
    )
    return client