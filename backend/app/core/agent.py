# agent.py
import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Import your custom PostgreSQL tool and search tool
from app.core.tool import QueryPostgreSQLTool, SearchTool

def create_agent():
    """
    Creates a ReAct agent with your QueryPostgreSQLTool (for SQL queries)
    and SearchTool (for general dental questions), injecting schema details
    and instructions about disallowing irrelevant queries.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model="gpt-4o-mini",
        temperature=0
    )

    # Database schema details
    table_schema = """
    The database schema is as follows:

    Table: patients
     - id (serial, primary key)
     - name (VARCHAR(100), NOT NULL)
     - email (VARCHAR(100), UNIQUE)
     - phone (VARCHAR(20))
     - created_at (TIMESTAMP, defaults to CURRENT_TIMESTAMP)

    Table: appointments
     - id (serial, primary key)
     - patient_id (integer, NOT NULL, foreign key referencing patients(id))
     - appointment_date (DATE, NOT NULL)
     - appointment_time (TIME, NOT NULL)
     - notes (text)
     - created_at (TIMESTAMP, defaults to CURRENT_TIMESTAMP)
    """

    # Refined system prompt:
    system_prompt = f"""
    You are an AI assistant with access to two tools:

    1) QueryPostgreSQLTool: For running SQL queries on the PostgreSQL dental database.
       {table_schema}

    2) SearchTool: For answering general dental questions from the web. (e.g. cause of dental diseases, cures, tips, preventions).

    Rules:
    - If the user's query contains or references SQL (SELECT, INSERT, UPDATE, etc.), call QueryPostgreSQLTool.
    - If the user wants general dental info (causes, cures, tips, preventions), call SearchTool.
    - If the question is irrelevant to dental care or the database, politely refuse to answer, stating:
      "I only handle dental-related queries."
    - Return only final results (query results, search results, or a polite refusal). No extra commentary.
    """

    # Tools: DB for SQL queries, plus SearchTool for general dental info
    tools = [QueryPostgreSQLTool(), SearchTool()]

    agent = create_react_agent(
        llm,
        tools,
        state_modifier=system_prompt
    )
    return agent

def run_agent(user_message: str) -> str:
    """
    Runs the ReAct agent on a user message. Returns the final text from the agent.
    """
    agent = create_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    final_text = response["messages"][-1].content
    return final_text
