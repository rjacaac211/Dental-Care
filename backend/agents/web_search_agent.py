# backend/agents/web_search_agent.py
class WebSearchAgent:
    def search_information(self, query: str):
        # For now, return dummy data. Later integrate OpenAI or other search API.
        return {"results": f"Search results for `{query}` will appear here."}
    