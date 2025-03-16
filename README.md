# Dental Care — AI-Powered Oral Health Assistant

Dental Care is an AI-powered dental care web application that combines onsite dental clinic appointments with an online AI assistant. It uses **FastAPI** (backend), **React** (frontend), and a **ReAct AI Agent** built with **LangChain** and **LangGraph**, enabling the system to run SQL queries on a **PostgreSQL** database or answer general dental inquiries via web search. The platform supports voice input through **Deepgram**, maintains multi-turn dialogue context using ephemeral memory, and includes a file upload feature for oral images alongside a **MobileNetV2**-based computer vision model for oral disease classification. All chat interactions are persisted in **MongoDB Atlas**, ensuring conversation history remains intact even after a page reload.

## Table of Contents
- [Overview](#overview)
- [Demo](#demo)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation via Docker Compose](#setup--installation-via-docker-compose)
- [Usage](#usage)
- [Model Training & Experimentation](#model-training--experimentation)

## Overview
**RJ Dental Care** is both a **dental clinic** offering onsite appointments and an **online AI assistant** that can:
1. **Answer general dental questions** (via a search tool).
2. **Process voice input** by transcribing speech to text using Deepgram’s Speech-to-Text API.
3. **Execute SQL queries** on a PostgreSQL database (tables `patients` and `appointments`).
4. **Perform image-based oral disease classification** using a computer vision model.
5. **Maintain ephemeral conversation** context through an in-memory store.
6. **Persist chat history** by saving all chat messages (both user and bot) to MongoDB Atlas, ensuring that previous conversation history is loaded on page reload.

## Demo
Watch a short demo of Dental Care in action:

![Dental Care Demo](docs/demo/demo.gif)

## Features
- **Onsite Dental Clinic + AI Assistant**  
  Manage and schedule clinic appointments onsite while leveraging the AI’s capabilities online.
- **Voice-Enabled Chat Interface**  
  Supports voice input via Deepgram’s Speech-to-Text API.
- **LangChain ReAct Agent**  
  Interprets user queries, either calling the **PostgreSQL** tool for database actions or the **Search** tool for dental health info.
- **Computer Vision for Disease Prediction**  
  Identifies oral diseases from uploaded images using a dedicated computer vision model.
- **Ephemeral Memory**  
  Uses a `WindowMemoryManager` to store conversation context for multi-turn dialogues.
- **Chat History Persistence**  
  Saves all chat messages to **MongoDB Atlas** so that previous conversation history is automatically loaded on page reload.
- **Dockerized Deployment**  
  Frontend (React), backend (FastAPI), and database all run via Docker Compose for a seamless setup.

## Project Structure

```
Dental-Care-PH/
├── frontend/                               # React Frontend
│   └── src/
│   │   └── components/
│   │   │   ├── ChatBox.js                  # Chat UI (integrates voice input and chat history persistence)
│   │   │   ├── ImageUpload.js              # For uploading images (e.g. oral disease prediction)
│   │   │   └── Navbar.js                   # Navigation bar
│   │   └── pages/
│   │   │   ├── About.js
│   │   │   ├── Contact.js
│   │   │   ├── Home.js
│   │   │   └──Product.js
│   │   ├── App.css                         # CSS for App.js
│   │   ├── App.js                          # Main React component
│   │   ├── index.css                       # Global styles
│   │   ├── index.js                        # Renders <App /> to DOM
│   │   └── reportWebVitals.js
│   ├── Dockerfile                          # Docker config for React
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
├── backend/                                # FastAPI Backend
│   ├── app/
│   │   ├── main.py                         # FastAPI entry point
│   │   ├── api/
│   │   │   └── routes.py                   # Defines endpoints: /chat, /predict, /transcribe, /save_chat, /chat_history
│   │   ├── core/
│   │   │   ├── agent.py                    # ReAct agent w/ ephemeral memory
│   │   │   ├── tool.py                     # QueryPostgreSQLTool and SearchTool
│   │   │   ├── memory.py                   # WindowMemoryManager (in-memory conversation)
│   │   │   ├── chat_history_db.py          # MongoDB connection
│   │   │   └── oral_disease_classifier.py  # Computer vision model for oral disease classification
│   │   └── models/
│   │       └── oral_disease_model.h5       # Trained model for disease prediction
│   ├── Dockerfile                          # Docker config for FastAPI
│   └── requirements.txt                    # Python dependencies
├── database/
│   ├── init.sql                            # Initialization SQL (tables, data)
│   └── Dockerfile                          # Docker config for PostgreSQL container
├── docs/                                   # Documentation & media
│   ├── demo/
│   │   ├── demo.gif
│   │   └── demo.mp4
│   └── Oral Disease Classification Project Report.pdf
└── docker-compose.yml                      # Multi-container setup (frontend, backend, database)
```

## Setup & Installation via Docker Compose

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/RJ-Dental-Care-PH.git
   cd RJ-Dental-Care-PH
   ```

2. **Configure Environment Variables**
Create a `.env` file (or set system environment variables) with the following content, replacing the placeholders as needed:
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

    # Deepgram (for speech-to-text)
    DEEPGRAM_API_KEY=your_deepgram_api_key

    # MongoDB Atlas (for chat history persistence)
    MONGODB_URI=mongodb+srv://your_user:your_password@cluster0.mongodb.net/chat_history_db?retryWrites=true&w=majority
    ```
    > **Note**: Never commit real API keys to version control. In production, store these in a secure secrets manager.

3. **Run Docker Compose**
    ```bash
    docker compose up --build
    ```
    This starts containers for the backend, frontend, and database. The React UI is served at `http://localhost:3000`, and the FastAPI API is available at `http://localhost:8000`.

## Usage

RJ Dental Care provides an intelligent voice-supported chat interface for managing dental queries and appointments, as well as a tool for oral disease classification. Below are instructions on how to interact with the API:
- **Chat Endpoint** (`POST /api/chat`)
  - Send JSON:
  ```json
  {
    "session_id": "some-session-id",
    "message": "Please execute: SELECT * FROM appointments;"
  }
  ```
  - **Response**:
  ```json
  {
    "final_response": "Query Results: [...]"
  }
  ```
- **Speech-to-Text Endpoint** (`POST /api/transcribe`):
  - Use the record button in the chat UI to capture audio. The recorded audio is sent to Deepgram for transcription, and the resulting text is populated into the chat input.
- **Save Chat History Endpoint** (`POST /api/save_chat`):
  - ach chat message (user and bot) is saved to MongoDB Atlas, so that conversation history is automatically loaded when the page is reloaded.
- **Get Chat History Endpoint** (`GET /api/chat_history/{session_id}`):
  - The frontend fetches previous messages using the session ID (stored in localStorage) to display the conversation history on page load
- **Predict Endpoint** (`POST /api/predict`):
  - Upload an image to get a classification:
  ```json
  {
    "prediction": "Caries or Gingivitis",
    "confidence": 92.45
  }
  ```
- **Ephemeral Memory**
  - The frontend uses a session_id (e.g. localStorage) to maintain multi-turn dialogues in memory.

## Model Training & Experimentation
For details on how the oral disease classification model was developed, evaluated, and refined, please refer to the [training](training/) folder (and the [docs](docs/) folder for the detailed project report).
  > **Subfolder READMEs**:
  >  - For more details on the backend, see [backend/README.md](backend/README.md).
  >  - For more details on the frontend, see [frontend/README.md](frontend/README.md).
  >  - For more details on the database setup, see [database/README.md](database/README.md).
  >  - For additional documentation and demo resources, see [docs/README.md](docs/README.md).

---

With the onsite clinic and online AI assistant, **RJ Dental Care** provides comprehensive oral healthcare both in person and via an intelligent chat interface.
