from fastapi import FastAPI
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_es_client():
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

@app.get("/search/{keyword}")
async def search_articles(keyword: str):
    es = get_es_client()

    s = Search(using=es, index="houzz").query(
        "multi_match", query=keyword, fields=["uid", "title"]
    )
    response = s.execute()

    articles = []
    for hit in response:
        article = hit.to_dict()
        articles.append(article)

    return {"articles": articles}



# uvicorn main:app --reload