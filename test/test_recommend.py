import pytest
from typing import List
from test.utils import client


class TestRecommendRouter:
    @pytest.mark.parametrize(
        "user_query, expect_title",
        [
            (
                "What is AI?",
                [
                    "AI isn't as smart as you think — but it could be",
                    "The danger of AI is weirder than you think",
                    "6 big ethical questions about the future of AI ",
                ],
            ),
            (
                "I want to decorate my kitchen, suggestions?",
                [
                    "6 Ways to Amp Up Your Kitchen Style With Patterned Tile",
                    "11 Ways to Update Your Kitchen Without a Sledgehammer",
                    "12 Ways to Make Your Kitchen Look and Feel Bigger",
                ],
            ),
            (
                "Tell me about US president",
                [
                    "George W. Bush cries delivering eulogy for his father, George H.W. Bush (Full Eulogy)",
                    "Historians ranked all the presidents. See where they have Trump",
                    "George H.W. Bush dead at age 94",
                ],
            ),
        ],
    )
    def test_recommend_by_user(self, user_query: str, expect_title: List[str]):
        """ """
        # Since elasticmock QueryType doesn't support "script_score" query
        # This Test case will direct connect to the eral ES database for testing
        kanban, offset, limit = "hwf", 0, 3

        response = client.get(
            f"/recommend/by/user_query?q={user_query}&kanban={kanban}&offset={offset}&limit={limit}"
        )
        res = response.json()
        answer = [item["title"] for item in res]
        answer_fields = set(list(res[0].keys()))
        expect_common_fields = set(
            ["uid", "title", "details", "posted", "link", "tags"]
        )

        assert response.status_code == 200
        assert answer == expect_title
        assert expect_common_fields.issubset(answer_fields) is True

    @pytest.mark.parametrize("", [])
    def test_recommend_by_product(self):
        """ """
        pass
