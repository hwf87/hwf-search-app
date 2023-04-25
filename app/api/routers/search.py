from typing import List, Optional
from elasticsearch_dsl import Search
from fastapi import APIRouter, Query, Path

from config import settings
from api.schemas.schema import Items, KwSearch
from db.elastic import get_es_client
from utils.search_utils import parse_kw_search, parse_response_to_items

router = APIRouter(
    prefix="/search",
    tags=["search"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{kanban}")
async def kw_search(
    kanban: str = Path(..., title="Kanban Name", example=settings.ES_ALIAS),
    query: str = Query(
        "hello world",
        description="Search will based on this query string",
        min_length=3,
        max_length=200,
    ),
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int] = Query(10, ge=0, le=100),
) -> KwSearch:
    """ """
    es = get_es_client()
    search = Search(using=es, index=kanban)

    search = search.query(
        "multi_match", query=query, fields=["uid", "title", "details"]
    )
    search = search.suggest("my_sug", query, term={"field": "title"})
    search = search.highlight(
        "title",
        "details",
        pre_tags="<strong>",
        post_tags="</strong>",
        fragment_size=50,
        number_of_fragments=5,
    )
    search = search[offset : offset + limit]
    search.aggs.bucket("my_agg", "terms", field="tags")
    response = search.execute().to_dict()

    return parse_kw_search(response)


@router.get("/tag/{kanban}")
async def tag_search(
    kanban: str = Path(..., title="Kanban Name", example=settings.ES_ALIAS),
    tag: str = Query(
        "history",
        description="Search will based on this tag to filter",
        min_length=3,
        max_length=200,
    ),
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int] = Query(10, ge=0, le=50),
) -> List[Items]:
    """ """
    es = get_es_client()
    # search = Search(using=es, index=kanban)
    # search = search.filter("terms", tags=[tag])
    # search = search[offset : offset + limit]
    # response = search.execute().to_dict()

    query_body = {
        "query": {"bool": {"filter": {"term": {"tags": tag}}}},
        "from": offset,
        "size": limit,
    }
    response = es.search(index=kanban, body=query_body)
    response = dict(response)

    return parse_response_to_items(response)


@router.get("/semantic/{kanban}")
async def semantic_search():
    """ """

    return {"hello": "semantic"}


@router.get("/qanda/{kanban}")
async def qa_search():
    """ """

    return {"hello": "qanda"}
