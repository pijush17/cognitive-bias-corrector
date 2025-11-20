# Simple mock evidence fetcher for MVP; replace with real MCP tool or web scraper as needed.
import random

class EvidenceFetcher:
    def __init__(self):
        pass

    def search(self, query: str):
        # Mock returns small structured data
        examples = [
            {"title": "Laptop A - 8GB RAM - $350", "snippet": "Solid battery", "score": 7.8},
            {"title": "Laptop B - 16GB RAM - $700", "snippet": "Better screen", "score": 8.6},
        ]
        return {"query": query, "top_results": random.sample(examples, k=1)}
