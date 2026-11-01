# 🤖 AI Research Assistant

An intelligent **Multi-Agent AI Research Assistant** built using **Python, LangGraph, FastAPI, Streamlit, and Pydantic**. The system automates the research process by planning topics, retrieving information, extracting relevant content, verifying facts, summarizing findings, and generating structured Markdown reports.

---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

---

## Project Description

The AI Research Assistant is a workflow-driven application that leverages **LangGraph** to orchestrate multiple AI agents, each responsible for a specific stage of the research pipeline.

The application follows a modular architecture based on **SOLID principles**, **Dependency Injection**, and a shared **ResearchState** using **Pydantic**.

### Workflow

```
User Query
    │
    ▼
Planner Agent
    │
    ▼
Search Agent
    │
    ▼
Reader Agent
    │
    ▼
Fact Checker Agent
    │
    ▼
Summarizer Agent
    │
    ▼
Writer Agent
    │
    ▼
Markdown Research Report
```

LangGraph manages the execution flow while each agent updates a shared state object, making the system scalable, maintainable, and easy to extend.

---

## Features

- Multi-Agent Architecture using LangGraph
- Intelligent research planning
- Automated information retrieval
- Content extraction and processing
- Fact verification pipeline
- AI-powered summarization
- Markdown report generation
- Shared Pydantic ResearchState
- Dependency Injection architecture
- Centralized logging and workflow tracking
- Modular service-based design
- Extensible architecture for adding new agents and tools

---

## Project Structure

```
AI-Research-Assistant/
│
├── backend/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── search_agent.py
│   │   ├── reader_agent.py
│   │   ├── fact_checker_agent.py
│   │   ├── summarizer_agent.py
│   │   └── writer_agent.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── planning_service.py
│   │   ├── reader_service.py
│   │   ├── fact_checker_service.py
│   │   ├── summarization_service.py
│   │   ├── writer_service.py
│   │   └── logging_service.py
│   │
│   ├── models/
│   │   ├── research_state.py
│   │   ├── enums.py
│   │   └── log_entry.py
│   │
│   ├── tools/
│   │   ├── tool_manager.py
│   │   ├── wikipedia_tool.py
│   │   ├── web_search_tool.py
│   │   └── arxiv_tool.py
│   │
│   ├── workflow/
│   │   ├── graph.py
│   │   └── supervisor.py
│   │
│   └── api/
│       └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .env
```

---

## Dependencies

### Backend

- Python 3.12+
- FastAPI
- LangGraph
- LangChain
- Pydantic v2
- Uvicorn

### Frontend

- Streamlit

### AI

- OpenAI / Gemini
- LangChain

### Utilities

- python-dotenv
- requests
- beautifulsoup4
- markdown

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ai-research-assistant.git
```

Navigate to the project directory

```bash
cd ai-research-assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_api_key
GOOGLE_API_KEY=your_api_key
MODEL_NAME=gpt-4o-mini
```

Update any additional environment variables required for external tools or APIs.

---

## Usage

### Start the FastAPI backend

```bash
uvicorn backend.api.main:app --reload
```

### Start the Streamlit frontend

```bash
streamlit run frontend/app.py
```

Open the Streamlit application in your browser.

Enter a research topic such as:

```
Artificial Intelligence in Healthcare
```

The system will automatically:

1. Generate a research plan.
2. Search relevant sources.
3. Extract useful information.
4. Verify facts.
5. Summarize findings.
6. Generate a Markdown report.

---

## API Documentation

After running the backend, access the interactive API documentation:

### Swagger UI

```
http://localhost:8000/docs
```

### ReDoc

```
http://localhost:8000/redoc
```

Example API endpoint

```
POST /research
```

Request

```json
{
  "topic": "Artificial Intelligence"
}
```

Response

```json
{
  "status": "completed",
  "report": "Generated Markdown Report"
}
```

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature/new-feature
```

5. Create a Pull Request.

---

## Future Enhancements

- Parallel execution of search tasks
- Human-in-the-loop approval
- Multi-LLM support
- PDF and DOCX report generation
- Citation management
- Persistent checkpoints
- Vector database integration (ChromaDB/FAISS)
- RAG-based document retrieval
- Multi-language research support

---

## License

This project is licensed under the MIT License.
