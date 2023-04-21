from typing import List, Dict
from fastapi import APIRouter, Depends, Query, Body
from sentence_transformers import SentenceTransformer

from dependency import get_token_header
from config import settings

model = SentenceTransformer(settings.PRE_TRAIN_MODEL)

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
    embeddings = model.encode(s)
    embeddings = embeddings.tolist()

    return {"embeddings": embeddings}


@router.post("/multi_sentence")
async def get_multi_sentence_embeddings(
    input_setences: List[str] = Body(
        ...,
        example=["Hello world", "Thank gog is Friday!"]
    ),
) -> Dict[str, List[List[float]]]:
    """ """
    embeddings = model.encode(input_setences)
    batch_embeddings = embeddings.tolist()

    return {"embeddings": batch_embeddings}
