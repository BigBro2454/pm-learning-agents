import os
import json
import urllib.request
import urllib.parse
from .config import TAVILY_API_KEY

def search_web(query: str, num_results: int = 3) -> list[dict]:
    """
    Executes a web search for the given query.
    If TAVILY_API_KEY is available, uses the Tavily API.
    Otherwise, returns mock search results for learning/testing purposes.
    
    Args:
        query: The search query string.
        num_results: The number of results to retrieve.
        
    Returns:
        A list of dictionaries containing 'title', 'url', and 'snippet'.
    """
    print(f"[Searcher] Searching for: '{query}'")
    
    if TAVILY_API_KEY:
        try:
            return _tavily_search(query, num_results)
        except Exception as e:
            print(f"[Searcher] Error using Tavily API: {e}. Falling back to mock search.")
            return _mock_search(query)
    else:
        print("[Searcher] No TAVILY_API_KEY found. Using mock search results.")
        return _mock_search(query)

def _tavily_search(query: str, num_results: int) -> list[dict]:
    """
    Actual implementation of the Tavily Search API.
    """
    url = "https://api.tavily.com/search"
    data = json.dumps({
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
        "max_results": num_results
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
    formatted_results = []
    for r in result.get('results', []):
        formatted_results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", "")
        })
        
    return formatted_results

def _mock_search(query: str) -> list[dict]:
    """
    Returns mock search results for when the API isn't configured.
    This helps the agent proceed without network dependencies.
    """
    # Simple mock response that adapts to the query somewhat
    return [
        {
            "title": f"Understanding {query} - A Comprehensive Guide",
            "url": f"https://example.com/guide-{query.replace(' ', '-')}",
            "snippet": f"This guide explores the key concepts behind {query}. It involves multiple aspects including its history, impact on modern society, and future trends."
        },
        {
            "title": f"{query} Explained in 5 Minutes",
            "url": f"https://example.com/explain-{query.replace(' ', '-')}",
            "snippet": f"What is {query}? It's a fascinating topic that many experts are researching. Recent developments show promising advancements."
        },
        {
            "title": f"The Future of {query}",
            "url": f"https://example.com/future-{query.replace(' ', '-')}",
            "snippet": f"Experts predict that {query} will continue to evolve. Let's break down the main components and how they fit into the broader ecosystem."
        }
    ]
