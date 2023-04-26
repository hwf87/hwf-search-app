import pytest
from elasticmock import elasticmock
from test.utils import client, create_mock_es_data


class TestSearchRouter:
    @pytest.mark.parametrize(
        "kanban, query, expect",
        [
            ("houzz", "Pro Tips for Lighting 10 Rooms and Outdoor Areas", "136224262"),
            (
                "cnn",
                "Hear Fox News viewers react to Fox's settlement with Dominion",
                "CODo_9sxAC0",
            ),
            (
                "tedtalk",
                "Why do we eat popcorn at the movies?",
                "andrew_smith_why_do_we_eat_popcorn_at_the_movies",
            ),
            ("hwf", "Pro Tips for Lighting 10 Rooms and Outdoor Areas", "136224262"),
            (
                "hwf",
                "Hear Fox News viewers react to Fox's settlement with Dominion",
                "CODo_9sxAC0",
            ),
            (
                "hwf",
                "Why do we eat popcorn at the movies?",
                "andrew_smith_why_do_we_eat_popcorn_at_the_movies",
            ),
        ],
    )
    def test_kw_search(self, kanban: str, query: str, expect: set):
        """
        Since elasticmock doesn't support complex search as well as elasticsearch_dsl library
        Here we're connecting to teh real database for unit testing
        """
        offset, limit = 0, 3
        response = client.get(
            f"/search/{kanban}?query={query}&offset={offset}&limit={limit}"
        )
        res = response.json()
        items = res["items"]
        pagination = len(items)
        aggregations = res["aggregations"]
        suggestions = res["suggestions"]
        answer = items[0]["uid"]
        answer_fields = set(list(items[0].keys()))
        expect_common_fields = set(
            ["uid", "title", "details", "posted", "link", "tags"]
        )

        assert response.status_code == 200
        assert answer == expect
        assert pagination == limit
        assert type(aggregations) == list
        assert type(suggestions) == list
        assert expect_common_fields.issubset(answer_fields) is True

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
    def test_semantic_search(self):
        """ """
        pass

    @elasticmock
    @pytest.mark.parametrize("", [])
    def test_qa_search(self):
        """ """
        pass
