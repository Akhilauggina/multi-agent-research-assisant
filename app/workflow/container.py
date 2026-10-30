from app.agents.fact_checker_agent import FactCheckerAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.reader_agent import ReaderAgent
from app.agents.search_agent import SearchAgent
from app.agents.summarizer_agent import SummarizerAgent
from app.agents.writer_agent import WriterAgent
from app.clients.gemini_client import GeminiClient
from app.clients.llm_client import LLMClient
from app.clients.openai_client import OpenAIClient
from app.clients.wikipedia_client import WikipediaClient
from app.config.settings import settings
from app.models.enums import SourceType
from app.services.fact_checking_service import FactCheckingService
from app.services.llm_service import LLMService
from app.services.logging_service import LoggingService
from app.services.planning_service import PlanningService
from app.services.reader_service import ReaderService
from app.services.search_service import SearchService
from app.services.source_selection_service import SourceSelectionService
from app.services.summarization_service import SummarizationService
from app.services.writer_service import WriterService
from app.tools.tool_registry import ToolRegistry
from app.tools.wikipedia_tool import WikipediaTool
from app.workflow.research_workflow import ResearchWorkflow


def create_llm_client() -> LLMClient:
    """
    Creates and returns the appropriate LLM client based on configuration.
    Defaults to Gemini if configured, or OpenAI if chosen.
    """
    if settings.llm_provider.lower() == "gemini" or (settings.gemini_api_key and not settings.openai_api_key):
        return GeminiClient(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )
    return OpenAIClient(
        api_key=settings.openai_api_key or "YOUR_API_KEY",
        model=settings.openai_model,
    )


def create_workflow() -> ResearchWorkflow:
    """
    Factory function wiring all clients, services, tools, and agents
    using dependency injection, returning the compiled ResearchWorkflow.
    """
    # 1. Clients
    llm_client = create_llm_client()
    wikipedia_client = WikipediaClient()

    # 2. Tools & ToolRegistry
    wikipedia_tool = WikipediaTool(client=wikipedia_client)
    tool_registry = ToolRegistry()
    tool_registry.register(source=SourceType.WIKIPEDIA, tool=wikipedia_tool)

    # 3. Services
    logging_service = LoggingService()
    llm_service = LLMService(llm_client=llm_client)

    planning_service = PlanningService(llm_service=llm_service)
    source_selection_service = SourceSelectionService()
    search_service = SearchService(tool_registry=tool_registry)
    reader_service = ReaderService(llm_service=llm_service)
    fact_checking_service = FactCheckingService(llm_service=llm_service)
    summarization_service = SummarizationService(llm_service=llm_service)
    writer_service = WriterService(llm_service=llm_service)

    # 4. Agents
    planner_agent = PlannerAgent(
        planning_service=planning_service,
        logging_service=logging_service,
    )
    search_agent = SearchAgent(
        search_service=search_service,
        source_selection_service=source_selection_service,
        logging_service=logging_service,
    )
    reader_agent = ReaderAgent(
        reader_service=reader_service,
        logging_service=logging_service,
    )
    fact_checker_agent = FactCheckerAgent(
        fact_checking_service=fact_checking_service,
        logging_service=logging_service,
    )
    summarizer_agent = SummarizerAgent(
        summarization_service=summarization_service,
        logging_service=logging_service,
    )
    writer_agent = WriterAgent(
        writer_service=writer_service,
        logging_service=logging_service,
    )

    # 5. Assemble Workflow
    return ResearchWorkflow(
        planner_agent=planner_agent,
        search_agent=search_agent,
        reader_agent=reader_agent,
        fact_checker_agent=fact_checker_agent,
        summarizer_agent=summarizer_agent,
        writer_agent=writer_agent,
    )
