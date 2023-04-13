import os
import sys
from fastapi import APIRouter, Depends, Query, Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date
from db.elastic import get_es_client
from dependency import get_token_header
from config import settings
from api.schemas.schema import Items

print(sys.path)

router = APIRouter(
    prefix="/search",
    tags=["search"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


def parse_response_to_items(response: Dict[str, Any]) -> List[Items]:
    """ """
    list_of_format_items = [
        {
            "uid": meta["_source"].get("uid", ""),
            "title": meta["_source"].get("title", ""),
            "details": meta["_source"].get("details", ""),
            "tags": meta["_source"].get("tags", []),
            "posted": meta["_source"].get("posted", ""),
            "link": meta["_source"].get("link", ""),
            "highlight": meta.get("highlight", {})
        }
        for meta in response["hits"]["hits"]
    ]

    return list_of_format_items


def parse_aggregations():
    """ """
    return ""

def parse_suggestions():
    """ """
    return ""

@router.get("/{kanban}")
async def kw_search(
        kanban: str = Path(
            ...,
            title = "Tag Name"
        ),
        query: str = Query(
            "hello world",
            description="Search will based on this query string",
            min_length=3,
            max_length=200,
        ), 
        offset: Optional[int] = Query(0, ge=0), 
        limit: Optional[int] = Query(10, ge=0, le=100)):
    es = get_es_client()
    search = Search(using=es, index=kanban)
    
    search = search.query("multi_match", query=query, fields=["uid", "title", "details"])
    search = search.suggest('my_suggestion', 'Desinger', term={'field': 'title'})
    search = search.highlight('title', 'details', pre_tags='<strong>', post_tags='</strong>', fragment_size=50, number_of_fragments=3)
    search = search[offset:offset+limit]
    search.aggs.bucket('agg', 'terms', field='tags')

    # create a multi-fields aggregation
    # multi_fields_agg = MultiTerms(fields=["field1", "field2", "field3"])
    # terms_agg = Terms(field="category")

    # add the multi-fields aggregation to the search object
    # search.aggs.bucket("my_agg", terms_agg)

    response = search.execute()

    articles = []
    for hit in response:
        article = hit.to_dict()
        articles.append(article)

    response = response.to_dict()
    aggregations = response["aggregations"]["agg"]["buckets"]
    suggestion = response["suggest"]["my_suggestion"]

    # return {"aggregations": aggregations, "articles": articles}
    return response

@router.get("/tag/{name}")
async def tag_search(
        name: str = Path(
            ...,
            title = "Tag Name"),
        offset: Optional[int] = Query(0, ge = 0), 
        limit: Optional[int] = Query(10, ge = 0, le = 50),
        example = "history") -> List[Items]:
    """ """
    es = get_es_client()
    search = Search(using = es, index = settings.ES_ALIAS)
    search = search.filter('terms', tags = [name])
    search = search[offset: offset + limit]
    response = search.execute().to_dict()

    return parse_response_to_items(response)

@router.get("/semantic")
async def semantic_search():
    """ """

    return {"hello": "search"}

@router.get("/qanda")
async def qa_search():
    """ """

    return {"hello": "search"}