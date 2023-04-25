import pytest
from elasticmock import elasticmock
from test.utils import client, create_mock_es_data


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
