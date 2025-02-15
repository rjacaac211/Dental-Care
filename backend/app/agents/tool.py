import os
import psycopg2
from pydantic import Field
from langchain_core.tools.base import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults

class QueryPostgreSQLTool(BaseTool):
    name: str = "QueryPostgreSQLTool"
    description: str = (
        "Execute SQL queries against a PostgreSQL database. "
        "Input: a valid SQL query. Output: query results or a confirmation message."
    )

    db_conn_str: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://your_username:your_password@database:5432/rj_dental_db")
    )

    def _run(self, tool_input: str) -> str:
        try:
            with psycopg2.connect(self.db_conn_str) as conn:
                with conn.cursor() as cur:
                    cur.execute(tool_input)
                    if tool_input.strip().lower().startswith("select"):
                        rows = cur.fetchall()
                        cols = [desc[0] for desc in cur.description]
                        results = [dict(zip(cols, row)) for row in rows]
                        return f"Query Results: {results}"
                    else:
                        conn.commit()
                        return "Query executed successfully."
        except Exception as e:
            return f"DBTool error: {str(e)}"

    async def _arun(self, tool_input: str) -> str:
        """For async usage if needed."""
        raise NotImplementedError("Async not implemented for QueryPostgreSQLTool.")

class SearchTool(BaseTool):
    name: str = "SearchTool"
    description: str = (
        "Perform a web search using Tavily. "
        "Input: A search query. Output: web search results."
    )
    search: TavilySearchResults = Field(default_factory=lambda: TavilySearchResults(max_results=5))

    def _run(self, tool_input: str) -> str:
        try:
            results = self.search.run(tool_input)
            return f"Search Results: {results}"
        except Exception as e:
            return f"SearchTool error: {str(e)}"

    async def _arun(self, tool_input: str) -> str:
        """For async usage if needed."""
        raise NotImplementedError("Async not implemented for SearchTool")
