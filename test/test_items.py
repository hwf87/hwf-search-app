import pytest
from elasticmock import elasticmock
from test.utils import client, create_mock_es_data


class TestItemsRouter:
    @elasticmock
    @pytest.mark.parametrize(
        "item_id, kanban, expect_title",
        [
            ("136224262", "houzz", "Pro Tips for Lighting 10 Rooms and Outdoor Areas"),
            (
                "andrew_smith_why_do_we_eat_popcorn_at_the_movies",
                "tedtalk",
                "Why do we eat popcorn at the movies?",
            ),
            (
                "CODo_9sxAC0",
                "cnn",
                "Hear Fox News viewers react to Fox's settlement with Dominion",
            ),
        ],
    )
    def test_get_item_info(self, item_id: str, kanban: str, expect_title: str):
        """ """
        # createe mock data [houzz, cnn, tedtalk]
        create_mock_es_data()

        # mock test
        response = client.get(f"/items/{item_id}?kanban={kanban}")
        res = response.json()
        answer = res[0]["title"]
        answer_fields = set(list(res[0].keys()))
        expect_common_fields = set(
            ["uid", "title", "details", "posted", "link", "tags"]
        )

        assert response.status_code == 200
        assert answer == expect_title
        assert expect_common_fields.issubset(answer_fields) is True
