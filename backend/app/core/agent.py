import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Tools
from app.core.tool import QueryPostgreSQLTool, SearchTool
from app.core.memory import WindowMemoryManager

# Create a single memory store for ephemeral usage
memory_store = WindowMemoryManager(window_size=10)

def create_agent():
    """
    Creates a ReAct agent with ephemeral window memory in mind.
    This agent uses tools QueryPostgreSQLTool (for SQL queries)
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

def run_agent(session_id: str, user_message: str) -> str:
    """
    Runs the ReAct agent on a user message, storing context in ephemeral memory.
    :param session_id: Unique session ID (e.g., from user or UI).
    :param user_message: The latest user message.
    :return: The agent's final text response.
    """
    agent = create_agent()

    # Load conversation from memory
    conversation_history = memory_store.load_conversation(session_id)

    # Convert to the expected format: [("human", "..."), ("assistant", "..."), ...]
    past_messages = []
    for msg in conversation_history:
        if msg["role"] == "user":
            past_messages.append(("human", msg["content"]))
        else:
            past_messages.append(("assistant", msg["content"]))

    # Add new user message
    past_messages.append(("human", user_message))
    memory_store.save_user_message(session_id, user_message)

    # Now pass these messages to the agent
    response = agent.invoke({"messages": past_messages})
    final_text = response["messages"][-1].content

    # Save the assistant's response
    memory_store.save_assistant_message(session_id, final_text)

    return final_text

def clear_session(session_id: str):
    """
    Clears the ephemeral conversation for a given session_id.
    """
    memory_store.clear_conversation(session_id)

