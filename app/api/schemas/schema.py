from typing import List, Dict, Optional
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 


class Items(BaseModel):
    uid: str
    title: str
    details: str
    posted: str
    tags: List[str]
    link: str
    highlight: Optional[Dict]

class HouzzItems(Items):
    author: str
    related_tags: List[str]
    description: str

class CnnItems(Items):
    channel: str
    comment_count: str
    likes: str
    views: str

class TedtalkItems(Items):
    author: str
    views: str

# class HighlightObj(BaseModel):
#     highlight: Dict

class AggregationObj(BaseModel):
    aggregation: Dict

class SuggestionObj(BaseModel):
    suggestion: Dict

class KwSearch(BaseModel):
    items: Items
    aggregation: Dict
    suggestion: Dict