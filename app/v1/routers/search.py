import os
import sys
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 
from db.elastic import get_es_client
from dependency import get_token_header

print(sys.path)

router = APIRouter(
    prefix="/search",
    tags=["search"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("")
async def kw_search(
        index_name: str = Query(
            "hwf",
            description="Search index name",
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
    s = Search(using=es, index=index_name)
    
    s = s.query("multi_match", query=query, fields=["uid", "title", "details"])
    s = s.source(exclude=["embeddings"])
    s = s.suggest('my_suggestion', 'Desinger', term={'field': 'title'})
    s = s.highlight('title', 'details', pre_tags='<strong>', post_tags='</strong>', fragment_size=50, number_of_fragments=3)
    s = s[offset:offset+limit]
    s.aggs.bucket('per_category', 'terms', field='tags')
    
    response = s.execute()

    articles = []
    for hit in response:
        article = hit.to_dict()
        articles.append(article)

    response = response.to_dict()
    aggregations = response["aggregations"]["per_category"]["buckets"]
    suggestion = response["suggest"]["my_suggestion"]

    # return {"aggregations": aggregations, "articles": articles}
    return response

@router.get("/filter")
async def filter_search():
    """ """

    return {"hello": "search"}

@router.get("/semantic")
async def semantic_search():
    """ """

    return {"hello": "search"}

@router.get("/qanda")
async def qa_search():
    """ """

    return {"hello": "search"}