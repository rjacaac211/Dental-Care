# RJ Dental Care PH

A simple AI-powered dental care application using **FastAPI** (for backend), **React** (for frontend), and **LangChain** for a ReAct agent that can either execute SQL queries on a PostgreSQL database or handle general dental search queries. It also includes ephemeral memory for multi-turn dialogues and a computer vision agent for oral disease prediction.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation via Docker Compose](#setup--installation-via-docker-compose)
- [Usage](#usage)

## Overview
RJ Dental Care PH is an AI assistant that:
1. **Executes SQL queries** on a PostgreSQL dental database (tables `patients` and `appointments`).
2. **Answers general dental questions** (using a search tool).
3. **Maintains ephemeral conversation** context via an in-memory store.
4. **Performs image-based oral disease classification** using a computer vision model.

## Features
- **ReAct Agent**  
  Uses [LangChain’s `create_react_agent`](https://python.langchain.com/docs/) to interpret user queries and decide whether to call the **PostgreSQL** tool or the **Search** tool.
- **Ephemeral Memory**  
  Implements a `WindowMemoryManager` that keeps conversation context in memory for each user session.
- **React Frontend**  
  Provides a chat UI that connects to the `/chat` endpoint. Supports image upload to `/predict`.
- **Dockerized**  
  Both frontend and backend run as containers via Docker Compose.

## Project Structure
```bash
RJ-Dental-Care-PH/
├── frontend/                           # React Frontend
│   └── src/
│   │   └── components/
│   │   │   ├── ChatBox.js             # Chat UI, connects to /chat endpoint
│   │   │   ├── ImageUpload.js         # For uploading images (e.g. oral disease prediction)
│   │   │   ├── Navbar.js              # Navigation bar
│   │   └── pages/
│   │   │   ├── About.js
│   │   │   ├── Contact.js
│   │   │   ├── Home.js
│   │   │   ├── Product.js
│   │   ├── App.css                    # CSS for App.js
│   │   ├── App.js                     # Main React component
│   │   ├── App.test.js
│   │   ├── index.css                  # Global styles
│   │   ├── index.js                   # Renders <App /> to DOM
│   │   ├── reportWebVitals.js
│   │   ├── setupTests.js
│   ├── Dockerfile                     # Docker config for React
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
├── backend/                           # FastAPI Backend
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── api/
│   │   │   └── routes.py             # Defines /chat, /predict endpoints
│   │   ├── core/
│   │   │   ├── agent.py              # Single ReAct agent w/ ephemeral memory
│   │   │   ├── tool.py               # QueryPostgreSQLTool + optional SearchTool
│   │   │   ├── memory.py             # WindowMemoryManager (in-memory conversation)
│   │   │   └── cv_agent.py           # CV agent for oral disease classification
│   │   └── models/
│   │       └── oral_disease_model.h5 # Trained model for disease prediction
│   ├── Dockerfile                     # Docker config for FastAPI
│   ├── requirements.txt              # Python dependencies
├── database/
│   ├── init.sql                       # Initialization SQL (tables, data)
│   ├── Dockerfile                     # Docker config for PostgreSQL container
├── docker-compose.yml                 # Multi-container setup (frontend, backend, DB)
└── README.md                          # Project documentation
```

## Setup & Installation via Docker Compose
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/RJ-Dental-Care-PH.git
   cd RJ-Dental-Care-PH

2. Configure Environment Variables
Create a .env file (or set system environment variables) with the following content, replacing the placeholders as needed:
    ```bash
    # .env
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
    ```
    Note:
    - Never commit real API keys to version control.
    - In production or CI/CD, store these in a secrets manager or environment variable store.

3. Run Docker Compose
    ```bash
    docker compose up --build
    ```
    This starts containers for the backend, frontend, and database. The React UI is served at http://localhost:3000, and the FastAPI API is available at http://localhost:8000.
    
## Usage
- Chat Endpoint:
    - `POST /api/chat` with JSON body `{ "session_id": "...", "message": "..." }`
    - Receives the final AI response:
    ```json
    {
        "final_response": "Query Results: [...]"
    }
    ```
- Predict Endpoint (CV agent for oral disease classification):
    - `POST /api/predict` with an uploaded image.
    - Returns JSON with `{"prediction": "...", "confidence": ...}`.
- Ephemeral Memory:
    - The frontend stores a session_id (e.g. in localStorage) to maintain conversation context across messages.
