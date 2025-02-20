# RJ Dental Care PH — Backend

This **FastAPI**-based backend provides core services for the RJ Dental Care PH application, including:
- A ReAct AI Agent (via **LangChain** and **LangGraph**) to handle dental inquiries (SQL queries or general info).
- Speech-to-text transcription using **Deepgram**.
- A computer vision model for oral disease classification.
- Chat history persistence in **MongoDB**.

## Table of Contents
- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Endpoints](#endpoints)
- [How It Works](#how-it-works)

## Overview

The **backend** comprises:
- **FastAPI** application, exposing RESTful endpoints for chatbot interactions, speech-to-text, and oral disease classification.
- **LangChain + LangGraph** ReAct Agent, which can either execute SQL queries on a PostgreSQL database or perform web searches for general dental questions.
- **Deepgram** integration for speech-to-text functionality.
- **MongoDB** for storing conversation history, ensuring that past chats are retained across sessions.
- **TensorFlow** model (`oral_disease_model.h5`) for classifying oral diseases based on uploaded images.

## Folder Structure

```
backend/
├── Dockerfile                          # Docker configuration for building the FastAPI image
├── requirements.txt                    # List of Python dependencies
└── app/
    ├── main.py                         # FastAPI entry point, sets up routes & CORS
    ├── api/
    │   └── routes.py                   # REST endpoints for chat, transcribe, predict, etc.
    ├── core/
    │   ├── agent.py                    # ReAct agent setup (integrates memory & tools)
    │   ├── tool.py                     # Tools for the agent (e.g., PostgreSQL & Search)
    │   ├── memory.py                   # Ephemeral memory manager for conversation context
    │   ├── chat_history_db.py          # MongoDB setup for storing chat history
    │   └── oral_disease_classifier.py  # Oral disease classification
    └── models/
        └── oral_disease_model.h5       # MobilenetV2-based TensorFlow model
```

## Setup & Installation

1. **Install Dependencies**
   If you're **not** using Docker Compose and want to run the backend standalone, install dependencies via:
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Run with Docker**
    The recommended approach is to use Docker (or Docker Compose) for a consistent environment:
    ```bash
    cd backend
    docker compose up -d --build backend
    ```
    This starts the FastAPI application on port `8000`.

    > **Note:** Typically, this backend is part of a multi-container setup (alongside the frontend and database), orchestrated by Docker Compose. 
    > Refer to the project's main [README](../README.md) for details on full-stack deployment.

## Environment Variables

In order for the backend to function properly, you must set the following environment variables (typically stored in a `.env` file or injected by your deployment environment). Below is an example `.env` file with placeholder values:

```bash
# FastAPI settings
DEBUG=True

# Database settings
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=rj_dental_db

# OpenAI API Key
OPENAI_API_KEY=sk-YourOpenAIKeyHere

# LangChain
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_YourLangChainKey
LANGSMITH_PROJECT="rj-dental-care-backend"

# Tavily
TAVILY_API_KEY=tvly-YourTavilyKeyHere

# Deepgram (for speech-to-text)
DEEPGRAM_API_KEY=your_deepgram_api_key

# MongoDB Atlas (for chat history persistence)
MONGODB_URI=mongodb+srv://your_user:your_password@cluster0.mongodb.net/?retryWrites=true&w=majority
```
**Descriptions**:
- `DEBUG`: Enables debug mode in FastAPI (not recommended for production).
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Credentials and database name for your PostgreSQL instance.
- `OPENAI_API_KEY`: Required for the LangChain ReAct agent that uses OpenAI models.
- `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGSMITH_PROJECT`: Required for LangChain usage and tracing support.
- `TAVILY_API_KEY`: Used by the `SearchTool` to perform web-based searches.
- `DEEPGRAM_API_KEY`: Auth token for sending audio clips to Deepgram for transcription.
- `MONGODB_URI`: Connection string to persist chat history in MongoDB Atlas.
    > **Important**: Never commit real API keys or passwords to public repositories. Use a secure secrets manager or environment variable approach in production.

## Endpoints

All endpoints are grouped under the `/api` prefix.

1. **Chat**  
   **`POST /api/chat`**  
   - **Request Body**:
     ```json
     {
       "session_id": "some-session-id",
       "message": "Your query or question here"
     }
     ```
   - **Response**:
     ```json
     {
       "final_response": "Agent's answer or query result"
     }
     ```

2. **Speech-to-Text**  
   **`POST /api/transcribe`**  
   - Accepts an audio file (via `multipart/form-data`) and returns a transcription from Deepgram.
   - **Form Fields**:
     - `file`: The uploaded audio file.
     - `session_id`: A unique identifier for the chat session.

3. **Predict Oral Disease**  
   **`POST /api/predict`**  
   - Accepts an image (via `multipart/form-data`) and returns a prediction (e.g., "Caries" or "Gingivitis") along with confidence percentage.

4. **Save Chat**  
   **`POST /api/save_chat`**  
   - Persists a chat message (from user or bot) to MongoDB.
   - **Request Body**:
     ```json
     {
       "session_id": "some-session-id",
       "sender": "user_or_bot",
       "message": "The message content"
     }
     ```

5. **Get Chat History**  
   **`GET /api/chat_history/{session_id}`**  
   - Retrieves all past chat messages for a given `session_id` from MongoDB.

## How It Works

1. **ReAct AI Agent**
    - The agent is created in `agent.py` using `create_react_agent` from **LangGraph**.
    - It uses two tools:
        - `QueryPostgreSQLTool`: Executes SQL queries against the PostgreSQL database.
        - `SearchTool`: Performs web searches (powered by Tavily) for general dental information.

2. **Ephemeral Memory**
    - The conversation is managed in-memory using a window memory mechanism (see `memory.py`).
    - A number of messages is stored for each session to maintain context.

3. **Speech-to-Text**
    - Audio files are sent to Deepgram for transcription via the `/transcribe` endpoint, then displayed in the chat UI.

4. **Computer Vision for Oral Disease Classification**
    - Uses a MobileNetV2-based model (`oral_disease_model.h5`) to classify images into "Caries" or "Gingivitis".

5. **Chat History Persistence**
    - All messages are also stored in MongoDB (see `chat_history_db`.py) so the chat history can be reloaded when the user returns.

