from itertools import count
import json

from httpx import HTTPError, request
from settings import settings
from urllib.request import Request, urlopen


def web_search(query: str, count: int = 3) -> dict:
    """
    Perform a web search using the LangSearch API.

    Args:
        query (str): The search query.
        count (int): The number of results to return.

    Returns:
        dict: The search results in JSON format.
    """

    if not query.strip():
        raise ValueError("query must be non-empty")

    payload = {
        "query": query,
        "count": max(1, min(count, 50)),
        "contents": {"text": {"maxCharacters": 3000}},
        "freshness": "noLimit",
    }


    request = Request(
        url="https://api.langsearch.com/v1/web-search",
        data=json.dumps(payload).encode("utf-8"),
        headers = {
                "Authorization": f"Bearer {settings.LANGSEARCH_API_KEY.get_secret_value()}",
                "Content-Type": "application/json"
            },
        method="POST"
    )

    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LangSearch request failed ({e.code}): {body}") from e

    items = result["data"]["webPages"]["value"]

    return {
        "input_tokens" : result["usage"]["input_tokens"],
        "output_tokens" : result["usage"]["output_tokens"],
        "sources": [
            {
                "name" : item.get("name"),
                "url": item.get("url"),
                "content": item.get("text") or item.get("snippet") or "",
                "date_published": item.get("datePublished")
            }
            for item in items
        ],
    }

if __name__ == "__main__":
    query = "What is the capital of France?"
    result_count = 5
    try:
        results = web_search(query, result_count)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error during web search: {e}")