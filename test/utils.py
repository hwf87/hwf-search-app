import json
from fastapi.testclient import TestClient
from typing import Iterator, Mapping, Union
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
        self.schema = read_json_data(path=schema_path)
        self.mock_data = read_json_data(path=data_path)

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


def read_json_data(path: str) -> json:
    f = open(path)
    json_data = json.load(f)
    return json_data


def create_mock_es_data():
    base_path = "./test/mock_es_data"
    mock_map = {
        "houzz": {
            "data": f"{base_path}/houzz_data_mock.json",
            "schema": f"{base_path}/houzz_schema.json",
        },
        "cnn": {
            "data": f"{base_path}/cnn_data_mock.json",
            "schema": f"{base_path}/cnn_schema.json",
        },
        "tedtalk": {
            "data": f"{base_path}/tedtalk_data_mock.json",
            "schema": f"{base_path}/tedtalk_schema.json",
        },
    }
    for index_name, val in mock_map.items():
        MED = MockEsData(
            test_index=index_name, schema_path=val["schema"], data_path=val["data"]
        )
        MED.execute()
