from typing import List, Dict, Any
from api.schemas.schema import Items


def parse_response_to_items(response: Dict[str, Any]) -> List[Items]:
    """ """
    list_of_format_items = [
        {
            "uid": meta["_source"].get("uid", ""),
            "title": meta["_source"].get("title", ""),
            "details": meta["_source"].get("details", ""),
            "tags": meta["_source"].get("tags", []),
            "posted": meta["_source"].get("posted", ""),
            "link": meta["_source"].get("link", ""),
            "highlight": meta.get("highlight", {}),
        }
        for meta in response["hits"]["hits"]
    ]

    return list_of_format_items


def parse_response_to_item_info(response: Dict[str, Any]) -> List[Items]:
    """ """
    item_info = [meta["_source"] for meta in response["hits"]["hits"]]
    return item_info


def parse_aggregations(response: Dict[str, Any]) -> List[Dict]:
    """ """
    aggregations_result = response["aggregations"]["my_agg"]["buckets"]
    return aggregations_result


def parse_suggestions(response: Dict[str, Any]) -> List[Dict]:
    """ """
    suggestions_result = response["suggest"]["my_sug"][0]["options"]
    return suggestions_result


def parse_kw_search(response: Dict[str, Any]) -> Dict[str, Any]:
    """ """
    kw_search_result = {
        "items": parse_response_to_items(response=response),
        "aggregations": parse_aggregations(response=response),
        "suggestions": parse_suggestions(response=response),
    }
    return kw_search_result
