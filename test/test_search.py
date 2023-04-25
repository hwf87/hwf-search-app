import json
import pytest
from fastapi.testclient import TestClient
from typing import Iterator, Mapping, Union
from elasticmock import elasticmock
from elasticsearch import Elasticsearch, helpers

import sys

sys.path[0] = sys.path[0] + "/app"
from db.elastic import get_es_client
from main import app

client = TestClient(app)


class MockEsData:
    def __init__(self, test_index: str, schema_path: str, data_path: str):
        self.es = get_es_client()
        self.test_index = test_index
        self.schema = self._read_json_data(path=schema_path)
        self.mock_data = self._read_json_data(path=data_path)

    def create_index(self, index_name: str, body: dict, es: Elasticsearch) -> None:
        """ """
        es.indices.create(index=index_name, body=body)

    def execute(self):
        """ """
        # create index
        self.create_index(index_name=self.test_index, body=self.schema, es=self.es)
        # insert mock data
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


def create_mock_es_data():
    mock_map = {
        "houzz": {
            "data": "./test/mock_data/houzz_data_mock.json",
            "schema": "./test/mock_data/houzz_schema.json",
        },
        "cnn": {
            "data": "./test/mock_data/cnn_data_mock.json",
            "schema": "./test/mock_data/cnn_schema.json",
        },
        "tedtalk": {
            "data": "./test/mock_data/tedtalk_data_mock.json",
            "schema": "./test/mock_data/tedtalk_schema.json",
        },
    }
    for index_name, val in mock_map.items():
        MED = MockEsData(
            test_index=index_name, schema_path=val["schema"], data_path=val["data"]
        )
        MED.execute()


@elasticmock
@pytest.mark.parametrize(
    "tag, expect",
    [("Kitchen Design", {"165919486", "128839992", "122561609", "80583370"})],
)
def test_tag_search(tag: str, expect: set):
    """ """
    # createe mock data
    create_mock_es_data()

    # mock test
    test_index = "houzz"
    response = client.get(f"/search/tag/{test_index}?tag={tag}&offset=0&limit=10")
    response = response.json()
    answer = set([item["uid"] for item in response])

    assert answer == set(expect)
