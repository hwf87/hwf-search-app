from pydantic import BaseModel
from typing import List, Dict, Optional


class Items(BaseModel):
    uid: str
    title: str
    details: str
    posted: str
    tags: List[str]
    link: str
    images: Optional[str]
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


class AggregationObj(BaseModel):
    key: str
    doc_count: int


class SuggestionObj(BaseModel):
    text: str
    score: float
    freq: int


class KwSearch(BaseModel):
    items: List[Items]
    aggregations: List[AggregationObj]
    suggestions: List[SuggestionObj]


class KanbanSchema(BaseModel):
    aliases: Optional[Dict]
    mappings: Dict
