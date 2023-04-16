from typing import Optional
from elasticsearch_dsl import Search
from fastapi import APIRouter, Query, Path, Depends

from config import settings
from db.elastic import get_es_client
from dependency import get_token_header
from utils.search_utils import parse_response_to_item_info


router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{item_id}")
async def get_item_info(
    item_id: str = Path(..., description="Item ID", example=125970555),
    kanban: Optional[str] = Query(settings.ES_ALIAS, title="Kanban Name"),
):
    """ """
    es = get_es_client()
    search = Search(using=es, index=kanban)
    search = search.filter("terms", uid=[item_id])
    search = search.source(excludes=["embeddings"])
    response = search.execute().to_dict()

    return parse_response_to_item_info(response)
