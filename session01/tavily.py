import json
import os

import httpx

TAVILY_URL = "https://api.tavily.com/search"
MAX_RESULTS = 5
TIMEOUT_SECONDS = 30.0


def web_search(payload):
    api_key = os.getenv("TAVILY_API_KEY")

    response = httpx.post(
        TAVILY_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=TIMEOUT_SECONDS,
    )
    
    results = [
        {
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
        }
        for result in response.json().get("results", [])
    ]
    return json.dumps(results)