import pytest
from typing import List
from test.utils import client, read_json_data


class TestInferenceRouter:
    @pytest.mark.parametrize(
        "sentence, test_data_path",
        [("hello world", "./test/test_data/helloworld_embedding.json")],
    )
    def test_get_sentence_embeddings(self, sentence: str, test_data_path: str):
        """ """

        response = client.get(f"/inference/sentence?s={sentence}")
        answer = response.json()["embeddings"]
        expect = read_json_data(test_data_path)["embeddings"]

        assert response.status_code == 200
        assert len(answer) == 384
        assert answer == expect

    @pytest.mark.parametrize(
        "multi_sentence, test_data_path",
        [
            (
                ["Hello world", "Thank god is Friday!"],
                "./test/test_data/helloworld_tgif_embedding.json",
            )
        ],
    )
    def test_get_multi_sentence_embeddings(
        self, multi_sentence: List, test_data_path: str
    ):
        """ """

        response = client.post("/inference/multi_sentence", json=multi_sentence)
        answer = response.json()["embeddings"]
        expect = read_json_data(test_data_path)["embeddings"]

        assert response.status_code == 200
        assert len(answer) == 2
        assert len(answer[0]) == 384
        assert len(answer[1]) == 384
        assert answer[0] == expect[0]
        assert answer[1] == expect[1]
