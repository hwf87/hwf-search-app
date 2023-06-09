from typing import List, Optional
from fastapi import APIRouter, Query

from db.elastic import get_es_client
from api.schemas.schema import Items
from config import settings
from utils.search_utils import infer_embeddings, parse_response_to_items


router = APIRouter(
    prefix="/recommend",
    tags=["recommend"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/by/product")
async def recommend_by_product():
    """ """
    return {"hello": "recommend by product"}


@router.get("/by/user_query")
async def recommend_by_user(
    q: str = Query(
        "hello world",
        description="Search will based on this query string",
        min_length=3,
        max_length=200,
    ),
    kanban: Optional[str] = Query(settings.ES_ALIAS),
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int] = Query(10, ge=0, le=100),
) -> List[Items]:
    """ """
    es = get_es_client()
    embeddings = infer_embeddings(q)
    query_body = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.embeddings, doc['embeddings']) + 1.0",
                    "params": {"embeddings": embeddings},
                },
            }
        },
        "from": offset,
        "size": limit,
    }
    response = es.search(index=kanban, body=query_body)
    response = dict(response)

    return parse_response_to_items(response)
