from typing import List, Dict
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 


class Product(BaseModel):
    title: str
    content: str
    created_at: str



class Items(BaseModel):
    uid = str
    title = str
    details = str
    posted = str
    tags = List[str]
    link = str