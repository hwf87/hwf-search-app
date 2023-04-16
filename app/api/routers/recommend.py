from typing import List, Optional
from elasticsearch_dsl import Search
from fastapi import APIRouter, Depends, Query

from db.elastic import get_es_client
from dependency import get_token_header


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


@router.get("/by/user")
async def by_user():
    """ """
    return {"hello": "recommend by user"}
