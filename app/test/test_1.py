import pytest
from typing import Iterator, Mapping, Union
from elasticmock import elasticmock
import elasticsearch
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json

from app.api.routers.search import tag_search

import sys

print(sys.path)


class FooService:
    def __init__(self):
        self.es = elasticsearch.Elasticsearch(
            "http://127.0.0.1:9200",
            http_auth=("elastic", "elastic"),
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


@elasticmock
def test_tag_search():
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

    assert 1 == 1
