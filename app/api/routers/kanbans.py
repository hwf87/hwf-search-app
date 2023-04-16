from typing import List, Optional
from elasticsearch_dsl import Search
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Query, Path, Body, Depends

from config import settings
from db.elastic import get_es_client
from dependency import get_token_header
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
        orderby: Optional[str] = Query("desc"),
        offset: Optional[int] = Query(0, ge=0), 
        limit: Optional[int] = Query(10, ge=0, le=50)) -> List[Items]:
    """ 
    """
    es = get_es_client()
    search = Search(using=es, index=kanban_name)
    search = search.sort({"posted": {"order": orderby}})
    search = search[offset : offset + limit]
    response = search.execute().to_dict()

    return parse_response_to_items(response)

@router.post("/{kanban_name}")
async def create_new_kanban(
        schema: KanbanSchema = Body(
            ...,
            example = {
                "aliases": {"alias_name": {}},
                "mappings": {
                    "properties": {
                        "field1": {"type": "keyword"},
                        "field2": {"type": "text"}
                    }
                }
            }
        ),
        kanban_name: str = Path(
            ...,
            title = "Kanban Name"
        )):
    """ """
    es = get_es_client()
    schema = jsonable_encoder(schema)
    res = es.indices.create(index=kanban_name, body=schema)

    return {
        "message": f"Successfully Create Kanban: {kanban_name}",
        "response": res
    }

@router.delete("/{kanban_name}")
async def delete_kanban(
        kanban_name: str = Path(
            ...,
            title = "Kanban Name"
        )):
    """ """
    es = get_es_client()
    res = es.indices.delete(index = kanban_name)

    return {
        "message": f"Successfully Delete Kanban: {kanban_name}",
        "response": res
    }

@router.put("/{kanban_name}/create/items/{item_id}")
@router.post("/{kanban_name}/create/items/{item_id}")
async def create_or_update_item_from_kanban(
        data: Items = Body(
            ...,
            example={
                "uid": "item-1234",
                "title": "Sample Item",
                "details": "This is a sample item",
                "posted": "2023-04-15",
                "tags": ["fastapi", "python", "web development"],
                "link": "https://example.com/sample-item",
                "highlight": {}
            }
        ),
        kanban_name: str = Path(
            ...,
            title = "Kanban Name"
        ),
        item_id: str = Path(
            ...,
            title = "Item Id"
        )):
    """ """
    es = get_es_client()
    data = jsonable_encoder(data)
    res = es.index(
        index = kanban_name,
        doc_type = "_doc",
        id = item_id, 
        body = data
    )

    return {
        "message": f"Successfully Create/Update Item: {item_id} from Kanban {kanban_name}",
        "response": res
    }

@router.delete("/{kanban_name}/delete/items/{item_id}")
async def delete_item_from_kanban(
        kanban_name: str = Path(
            ...,
            title = "Kanban Name"
        ),
        item_id: str = Path(
            ...,
            title = "Item Id"
        )):
    """ 
    """
    es = get_es_client()
    res = es.delete(index = kanban_name, doc_type = "_doc", id = item_id)

    return {
        "message": f"Successfully Delete Item: {item_id} from Kanban {kanban_name}",
        "response": res
    }