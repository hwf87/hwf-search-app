import pytest
from typing import Iterator, Mapping, Union
from elasticmock import elasticmock
from elasticsearch import Elasticsearch, helpers
import json
from fastapi.testclient import TestClient

import sys

sys.path[0] = sys.path[0] + "/app"

# from api.routers.search import tag_search
from db.elastic import get_es_client
from main import app

client = TestClient(app)


class MockEsData:
    def __init__(self, test_index, data_path):
        self.es = get_es_client()
        self.test_index = test_index
        self.mock_data = self._read_json_data(path=data_path)

    # TODO: create mappings
    # TODO: create index
    # TODO: create alias
    # TODO: create multi index at once

    def create(self):
        """ """
        if self.es and self.mock_data:
            self.bulk_insert(
                actions=self.load_action_batch(
                    op_type="index",
                    index_name=self.test_index,
                    documents=self.mock_data,
                ),
                es=self.es,
            )

    def _read_json_data(self, path: str) -> json:
        f = open(path)
        my_json_list = json.load(f)
        return my_json_list

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


@elasticmock
@pytest.mark.parametrize(
    "tag, expect",
    [("Kitchen Design", {"165919486", "128839992", "122561609", "80583370"})],
)
def test_tag_search(tag: str, expect: set):
    """ """
    test_index = "test_houzz"

    MED = MockEsData(
        test_index=test_index, data_path="./test/mock_data/houzz_data_mock.json"
    )
    MED.create()
    response = client.get(f"/search/tag/{test_index}?tag={tag}&offset=0&limit=10")
    response = response.json()
    answer = set([item["uid"] for item in response])

    assert answer == set(expect)
