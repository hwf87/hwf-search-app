import pytest
from elasticmock import elasticmock
from test.utils import client, create_mock_es_data


class TestSearchRouter:
    @elasticmock
    @pytest.mark.parametrize(
        "test_index, tag, expect",
        [
            (
                "houzz",
                "Kitchen Design",
                {"165919486", "128839992", "122561609", "80583370"},
            )
        ],
    )
    def test_tag_search(self, test_index: str, tag: str, expect: set):
        """ """
        # createe mock data [houzz, cnn, tedtalk]
        create_mock_es_data()

        # mock test
        response = client.get(f"/search/tag/{test_index}?tag={tag}")
        res = response.json()
        answer = set([item["uid"] for item in res])

        assert response.status_code == 200
        assert answer == set(expect)

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_kw_search(self):
        """ """
        pass

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_semantic_search(self):
        """ """
        pass

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_qa_search(self):
        """ """
        pass
