# Multi-Agent Research Assistant

A modular, clean architecture multi-agent research assistant built in Python 3.12+, LangGraph, FastAPI, and Streamlit, adhering to SOLID principles, dependency injection, and clean boundaries.

## Architecture

```
START ─► PlannerAgent ─► SearchAgent ─► ReaderAgent ─► FactCheckerAgent ─► SummarizerAgent ─► WriterAgent ─► END
```

### Flow of ResearchState

The application uses one shared Pydantic `ResearchState` container that flows through every LangGraph node:
* `topic`: User-defined research topic
* `plan`: Formulated section titles
* `sections`: Planned research section objects
* `search_results`: Raw tool outputs per section (`dict[str, list[ToolResult]]`)
* `read_results`: Cleaned and extracted factual text per section (`dict[str, str]`)
* `verified_results`: Factually verified information per section (`dict[str, str]`)
* `final_summary`: Synthesized cross-section plain text summary
* `report`: Final production-grade report formatted strictly in Markdown
* `logs`: Structured `LogEntry` records captured via `LoggingService`

### Agents & Services

1. **PlannerAgent** (`app/agents/planner_agent.py`)
   - Uses `PlanningService` (`app/services/planning_service.py`)
   - Decomposes the research topic into structured sections.
2. **SearchAgent** (`app/agents/search_agent.py`)
   - Uses `SourceSelectionService` and `SearchService` (`app/services/`)
   - Gathers information across tools registered in `ToolRegistry`.
3. **ReaderAgent** (`app/agents/reader_agent.py`)
   - Uses `ReaderService` (`app/services/reader_service.py`)
   - Cleans and extracts relevant content from `search_results` into `read_results`. Does not summarize or verify facts.
4. **FactCheckerAgent** (`app/agents/fact_checker_agent.py`)
   - Uses `FactCheckingService` (`app/services/fact_checking_service.py`)
   - Checks and retains verified factual assertions into `verified_results`.
5. **SummarizerAgent** (`app/agents/summarizer_agent.py`)
   - Uses `SummarizationService` (`app/services/summarization_service.py`)
   - Consolidates all verified sections into one concise plain-text `final_summary`.
6. **WriterAgent** (`app/agents/writer_agent.py`)
   - Uses `WriterService` (`app/services/writer_service.py`)
   - Authors the final comprehensive Markdown research `report`.
7. **LoggingService** (`app/services/logging_service.py`)
   - Decoupled logger injected into all agents. Never mutates `logs` directly from agents.

### Dependency Injection & Workflow

All clients, services, tools, and agents are assembled in `app/workflow/container.py` and orchestrated via `app/workflow/research_workflow.py` using `langgraph.graph.StateGraph`.

---

## Getting Started

### 1. Installation

```bash
create a folder multi-agent -research-assistant and naviagate to the path cd multi-agent -research-assistant
pip install -r requirements.txt
```

### 2. Configuration

Configure `.env`:

```env

GEMINI_API_KEY=your_gemini_api_key_here
LOG_LEVEL=INFO
```

### 3. Execution Options

#### Run via CLI Pipeline:
```bash
python -m app.main
```

#### Run FastAPI REST Backend:
```bash
uvicorn app.api.server:app --reload --port 8000
```
Interactive OpenAPI documentation will be available at `http://localhost:8000/docs`.

#### Run Streamlit Web Application:
```bash
streamlit run app/app.py
```
