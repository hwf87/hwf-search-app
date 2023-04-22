from typing import List, Dict
from fastapi import APIRouter, Query, Body

from utils.search_utils import infer_embeddings

router = APIRouter(
    prefix="/inference",
    tags=["inference"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/sentence")
async def get_sentence_embeddings(
    s: str = Query(
        "hello world",
        description="Get Single Sentence embeddings",
        min_length=1,
        max_length=200,
    ),
) -> Dict[str, List[float]]:
    """ """
    embeddings = infer_embeddings(s)

    return {"embeddings": embeddings}


@router.post("/multi_sentence")
async def get_multi_sentence_embeddings(
    input_setences: List[str] = Body(
        ..., example=["Hello world", "Thank gog is Friday!"]
    ),
) -> Dict[str, List[List[float]]]:
    """ """
    batch_embeddings = infer_embeddings(input_setences)

    return {"embeddings": batch_embeddings}
