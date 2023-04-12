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
    prefix="/kanbans",
    tags=["kanbans"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def get_all_kanbans():
    """ 
    """

    return {"hello": "kanbans"}

@router.get("/{kanban_name}/items")
async def get_items_from_kanban():
    """ 
    """

    return {"hello": "kanbans"}

@router.post("/{kanban_name}")
async def create_new_kanban():
    """ 
    """

    return {"hello": "kanbans"}

@router.post("/{kanban_name}/create/items/{item_id}")
async def create_item_from_kanban():
    """ 
    """

    return {"hello": "kanbans"}

@router.put("/{kanban_name}/update/items/{item_id}")
async def update_item_from_kanban():
    """ 
    """

    return {"hello": "kanbans"}

@router.delete("/{kanban_name}/delete/items/{item_id}")
async def delete_item_from_kanban():
    """ 
    """

    return {"hello": "kanbans"}