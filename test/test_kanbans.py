import pytest
from typing import List
from elasticmock import elasticmock
from test.utils import client, create_mock_es_data


class TestKanbansRouter:
    @pytest.mark.parametrize("expect", [(["cnn", "houzz", "tedtalk"])])
    def test_get_all_kanbans(self, expect: List[str]):
        """ """
        response = client.get("/kanbans")
        res = response.json()
        answer = res["kanbans"]

        assert response.status_code == 200
        assert answer == expect

    @elasticmock
    @pytest.mark.parametrize(
        "kanban_name, expect", [("houzz", "2023-04-07"), ("cnn", "2023-04-21")]
    )
    def test_get_items_from_kanban(self, kanban_name: str, expect: str):
        """ """
        # createe mock data [houzz, cnn, tedtalk]
        create_mock_es_data()

        response = client.get(
            f"/kanbans/{kanban_name}/items?orderby=desc&offset=0&limit=10"
        )
        res = response.json()
        print(res[0])
        answer = res[0]["posted"]

        assert response.status_code == 200
        assert answer == expect

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_create_new_kanban(self):
        """ """
        pass

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_delete_kanban(self):
        """ """
        pass

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_create_or_update_item_from_kanban(self):
        """ """
        pass

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_delete_item_from_kanban(self):
        """ """
        pass
