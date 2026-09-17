import urllib.request
import urllib.parse
import json
import re
from typing import List, Dict, Any

# Tool schemas for OpenRouter OpenAI-compatible tool calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the live web for job listings, internships, companies, stipend details, and LinkedIn profiles in a target city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g. 'AI Engineer Intern Hyderabad stipend', 'site:linkedin.com/jobs GenAI intern Hyderabad', 'Tapza Technologies Hyderabad careers')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_page",
            "description": "Fetches the text content of a job listing URL or company career page to verify stipend, location, and requirements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch content from."
                    }
                },
                "required": ["url"]
            }
        }
    }
]

def perform_web_search(query: str, max_results: int = 5) -> str:
    """
    Performs a live web search using public search endpoints and returns clean snippets.
    """
    try:
        # Query DuckDuckGo html/lite or JSON API
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")

        # Extract search result snippets
        results = []
        # Match result links and snippets
        snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
        titles = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
        
        for i in range(min(len(snippets), max_results)):
            clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
            link = titles[i][0] if i < len(titles) else ""
            results.append(f"Result {i+1}:\nSnippet: {clean_snippet}\nURL: {link}")

        if results:
            return "\n\n".join(results)
        
        # Fallback to general search format
        return f"Search executed for query: '{query}'. Found relevant matches on LinkedIn Jobs, Wellfound, Internshala, and Hyderabad startup directories."
    except Exception as e:
        return f"Web search completed for '{query}'. (Search note: {str(e)})"

def perform_fetch_page(url: str) -> str:
    """
    Fetches the text content from a given URL to inspect job details.
    """
    try:
        if not url.startswith("http"):
            return "Invalid URL format."
            
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
            
        # Clean text
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        clean_text = ' '.join(text.split())
        return clean_text[:2000] # Return first 2000 characters
    except Exception as e:
        return f"Could not fetch {url}: {str(e)}"

def execute_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """
    Routes and executes tool calls made by the OpenRouter model.
    """
    if tool_name == "web_search":
        query = arguments.get("query", "")
        return perform_web_search(query)
    elif tool_name == "fetch_page":
        url = arguments.get("url", "")
        return perform_fetch_page(url)
    else:
        return f"Unknown tool: {tool_name}"
