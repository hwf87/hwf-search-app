from fastapi import APIRouter, Depends, Query, Path, Request, Body
from typing import List, Optional, Dict
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Keyword, Date 
from db.elastic import get_es_client
from dependency import get_token_header
from config import settings
from api.schemas.schema import Items, KanbanSchema
from utils.search_utils import parse_response_to_items


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
    es = get_es_client()
    if es.indices.exists_alias(settings.ES_ALIAS):
        kanbans = list(es.indices.get(settings.ES_ALIAS).keys())
    return {"kanbans": kanbans}

@router.get("/{kanban_name}/items")
async def get_items_from_kanban(
        kanban_name: str = Path(
            ...,
            title = "kanban Name"
        ),
        offset: Optional[int] = Query(0, ge=0), 
        limit: Optional[int] = Query(10, ge=0, le=50)) -> List[Items]:
    """ 
    """
    es = get_es_client()
    search = Search(using=es, index=kanban_name)
    search = search.query("match_all")
    search = search[offset : offset + limit]
    response = search.execute().to_dict()

    return parse_response_to_items(response)

@router.post("/{kanban_name}")
async def create_new_kanban(
        request: Dict = Body(...),
        kanban_name: str = Path(
            ...,
            title = "kanban Name"
        )):
    """ 
    body = {
        name: Optional[str]
        alias: Optional[str]
        settings: Optional[Dict]
        mappings: Dict
        mappings = {
            "properties": {
                "field1": "type1",
                "field2": "type2"
            }
        }
    }
    """
    # data = KanbanSchema.parse_raw(await request.body())
    print(type(request))

    # data = request.json()
    # body = request["mappings"]

    # {
    #     "aliases": ft_.alias,
    #     "mappings": 
    # }

    es = get_es_client()
    res = es.indices.create(index=kanban_name, body=request)
    status_code = res.meta.status

    return {"status": status_code, "message": f"Create {kanban_name} Successfully."}

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