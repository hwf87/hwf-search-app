from typing import List, Optional
from elasticsearch_dsl import Search
from fastapi import APIRouter, Depends, Query

from db.elastic import get_es_client
from dependency import get_token_header
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
async def by_product():
    """ """
    return {"hello": "recommend by product"}


@router.get("/by/user_query")
async def by_user(
    q: str = Query(
        "hello world",
        description="Search will based on this query string",
        min_length=3,
        max_length=200,
    ),
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int] = Query(10, ge=0, le=100),
) -> List[Items]:
    """ """
    es = get_es_client()
    search = Search(using=es, index=settings.ES_ALIAS)

    embeddings = infer_embeddings(q)
    body = {
        "size": 10,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.embeddings, doc['embeddings']) + 1.0",
                    "params": {
                        "embeddings": embeddings
                    }
                }
            }
        }
    }
    search.update_from_dict(body)
    search = search[offset : offset + limit]
    response = search.execute().to_dict()

    return parse_response_to_items(response)
