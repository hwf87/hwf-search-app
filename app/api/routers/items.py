import os
import sys
from fastapi import APIRouter, Depends, Query, Path
from typing import List, Optional
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 
from db.elastic import get_es_client
from dependency import get_token_header

print(sys.path)

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def search_products(uid: str = Query(
            "125970555",
            description="Product ID",
        )):
    """ 
    """
    es = get_es_client()
    s = Search(using=es, index="hwf")
    s = s.filter('terms', uid=[uid])
    response = s.execute()
    response = response.to_dict()

    return response


@router.get("/{item_id}")
async def search_products(product_id: str):
    """ 
    """
    es = get_es_client()
    s = Search(using=es, index="hwf")
    s = s.filter('terms', uid=[item_id])
    response = s.execute()
    response = response.to_dict()

    return response

@router.get("/{item_id}/title")
async def search_products(item_id: str = Path(..., title="Product ID", description="The ID of the Product to get"), example="125970555"):
    """ 
    """
    es = get_es_client()
    s = Search(using=es, index="hwf")
    s = s.source(include=["title"])
    s = s.filter('terms', uid=[item_id])
    response = s.execute()
    response = response.to_dict()

    return response