import pytest
from typing import Iterator, Mapping, Union, List
from elasticmock import elasticmock
import elasticsearch
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
import asyncio

from fastapi.testclient import TestClient


import sys

sys.path[0] = sys.path[0] + "/app"
print(sys.path)

from api.routers.search import tag_search
from config import settings
from main import app

client = TestClient(app)


print(client)

print(settings.ES_HOST)


class FooService:
    def __init__(self):
        self.es = elasticsearch.Elasticsearch(
            "http://127.0.0.1:9200",
            verify_certs=False,
            timeout=30,
            max_retries=10,
            retry_on_timeout=True,
        )

    def load_action_batch(
        self, op_type: str, index_name: str, documents: list
    ) -> Mapping[str, Union[str, dict]]:
        """ """
        for document in documents:
            document_id = document["uid"]
            actions = {
                "_op_type": op_type,
                "_index": index_name,
                "_id": document_id,
                "_source": document,
            }
            yield actions

    def bulk_insert(self, actions: Iterator, es: Elasticsearch) -> None:
        """ """
        batches = []
        for _, meta in helpers.streaming_bulk(
            client=es,
            actions=actions,
            chunk_size=100,
            max_chunk_bytes=104857600,
            max_retries=3,
            yield_ok=True,
            raise_on_error=False,
            ignore_status=(),
        ):
            batches.append(meta)

    def create(self, index, body):
        es_object = self.es.index(index, body)
        return es_object.get("_id")


def read_json_data(path: str) -> json:
    f = open(path)
    my_json_list = json.load(f)
    return my_json_list


# @elasticmock
# def test_123():
#     """ """
#     FS = FooService()
#     my_json_list = read_json_data(path="./test/mock_data/houzz_data_mock.json")
#     if True:
#         FS.bulk_insert(
#             actions=FS.load_action_batch(
#                 op_type="index",
#                 index_name="test_houzz",
#                 documents=my_json_list,
#             ),
#             es=FS.es,
#         )

#     assert 1 == 1


@elasticmock
@pytest.mark.parametrize(
    "tag, expect",
    [("Kitchen Design", {"165919486", "128839992", "122561609", "80583370"})],
)
def test_tag_search(tag: str, expect: set):
    """ """
    FS = FooService()
    my_json_list = read_json_data(path="./test/mock_data/houzz_data_mock.json")
    if True:
        FS.bulk_insert(
            actions=FS.load_action_batch(
                op_type="index",
                index_name="test_houzz",
                documents=my_json_list,
            ),
            es=FS.es,
        )
    response = client.get(f"/search/tag/test_houzz?tag={tag}&offset=0&limit=10")
    response = response.json()
    answer = set([item["uid"] for item in response])
    # expect = set(["165919486", "128839992", "122561609", "80583370"])

    assert answer == set(expect)
