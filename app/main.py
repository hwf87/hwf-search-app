from fastapi import FastAPI
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 
from pydantic import BaseModel
from v1.routers import search, items, recommend, kanbans


app = FastAPI()

app.include_router(search.router)
app.include_router(items.router)
app.include_router(kanbans.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


# uvicorn main:app --reload