import pytest
from typing import List
from elasticmock import elasticmock
from test.utils import client, read_json_data


class TestKanbansRouter:
    @pytest.mark.parametrize("expect", [(["cnn", "houzz", "tedtalk"])])
    def test_get_all_kanbans(self, expect: List[str]):
        """ """
        response = client.get("/kanbans")
        res = response.json()
        answer = res["kanbans"]

        assert response.status_code == 200
        assert answer == expect

    @pytest.mark.parametrize(
        "kanban_name, orderby, expect",
        [
            ("houzz", "desc", "2023-04-07"),
            ("cnn", "desc", "2023-04-21"),
            ("tedtalk", "desc", "2023-04-01"),
            ("houzz", "asc", "2017-10-16"),
            ("cnn", "asc", "2018-02-27"),
            ("tedtalk", "asc", "2006-06-01"),
        ],
    )
    def test_get_items_from_kanban(self, kanban_name: str, orderby: str, expect: str):
        """ """
        offset, limit = 0, 3
        response = client.get(
            f"/kanbans/{kanban_name}/items?orderby={orderby}&offset={offset}&limit={limit}"
        )
        res = response.json()
        answer = res[0]["posted"]

        assert response.status_code == 200
        assert len(res) == limit
        assert answer == expect

    @elasticmock
    @pytest.mark.parametrize(
        "kanban_name, schema_path, expect",
        [
            (
                "happy_index",
                "./test/test_data/happy_index_schema.json",
                "Successfully Create Kanban: happy_index",
            )
        ],
    )
    def test_create_new_kanban(self, kanban_name: str, schema_path: str, expect: str):
        """
        === Sample Response ===
        {
            "message": "Successfully Create Kanban: happy_index",
            "response": {
                "acknowledged": true,
                "shards_acknowledged": true,
                "index": "happy_index"
            }
        }
        """
        schema = read_json_data(schema_path)
        response = client.post(f"/kanbans/{kanban_name}", json=schema)
        res = response.json()
        answer = res["message"]

        assert response.status_code == 200
        assert answer == expect

    @elasticmock
    @pytest.mark.parametrize(
        "kanban_name, expect",
        [
            (
                "happy_index",
                "Successfully Delete Kanban: happy_index",
            )
        ],
    )
    def test_delete_kanban(self, kanban_name: str, expect: str):
        """ """
        # create test index first
        schema_path = "./test/test_data/happy_index_schema.json"
        schema = read_json_data(schema_path)
        client.post(f"/kanbans/{kanban_name}", json=schema)

        # Delete test index
        response = client.delete(f"/kanbans/{kanban_name}")
        res = response.json()
        answer = res["message"]

        assert response.status_code == 200
        assert answer == expect

    @elasticmock
    @pytest.mark.parametrize(
        "kanban_name, item_id, data_path, expect",
        [
            (
                "happy_index",
                "123",
                "./test/test_data/happy_item.json",
                "Successfully Create/Update Item: 123 from Kanban happy_index",
            )
        ],
    )
    def test_create_or_update_item_from_kanban(
        self, kanban_name: str, item_id: str, data_path: str, expect: str
    ):
        """ """
        data = read_json_data(data_path)
        # put method to create
        put_response = client.put(
            f"/kanbans/{kanban_name}/create/items/{item_id}", json=data
        )
        put_res = put_response.json()
        put_answer = put_res["message"]
        put_version_1 = put_res["response"]["_version"]

        # post method to update value
        post_response = client.post(
            f"/kanbans/{kanban_name}/create/items/{item_id}", json=data
        )
        post_res = post_response.json()
        post_answer = post_res["message"]
        post_version_2 = post_res["response"]["_version"]

        assert put_response.status_code == 200
        assert put_answer == expect
        assert put_version_1 == 1
        assert post_response.status_code == 200
        assert post_answer == expect
        assert post_version_2 == 2

    @elasticmock
    @pytest.mark.parametrize(
        "kanban_name, item_id, expect",
        [
            (
                "happy_index",
                "123",
                "Successfully Delete Item: 123 from Kanban happy_index",
            )
        ],
    )
    def test_delete_item_from_kanban(self, kanban_name: str, item_id: str, expect: str):
        """ """
        # create item first
        data_path = "./test/test_data/happy_item.json"
        data = read_json_data(data_path)
        client.put(f"/kanbans/{kanban_name}/create/items/{item_id}", json=data)

        # Delete item
        response = client.delete(f"/kanbans/{kanban_name}/delete/items/{item_id}")
        res = response.json()
        answer = res["message"]

        assert response.status_code == 200
        assert answer == expect
