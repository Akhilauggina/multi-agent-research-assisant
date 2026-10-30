from app.models.enums import AgentType, LogLevel, TaskStatus, WorkflowStatus
from app.models.research_state import ResearchState
from app.models.tool_request import ToolRequest
from app.services.logging_service import LoggingService
from app.services.search_service import SearchService
from app.services.source_selection_service import SourceSelectionService


class SearchAgent:
    """
    Coordinates research information gathering across sections.
    Delegates source selection to SourceSelectionService and search execution
    to SearchService without containing any if/else source selection logic.
    Uses LoggingService for all logging needs.
    """

    def __init__(
        self,
        search_service: SearchService,
        source_selection_service: SourceSelectionService,
        logging_service: LoggingService | None = None,
    ) -> None:
        """
        Initializes SearchAgent with injected services.

        Args:
            search_service: Injected SearchService instance.
            source_selection_service: Injected SourceSelectionService instance.
            logging_service: Injected LoggingService instance.
        """
        self.search_service = search_service
        self.source_selection_service = source_selection_service
        self.logging_service = logging_service or LoggingService()

    def execute(self, state: ResearchState) -> ResearchState:
        """
        Executes information gathering for each section in ResearchState.
        Updates state.search_results and individual sections.

        Args:
            state: Active ResearchState containing planned sections.

        Returns:
            ResearchState: Updated state containing research results for each section.
        """
        self.logging_service.log(
            state=state,
            agent=AgentType.SEARCH,
            message=f"Starting search phase for topic: '{state.topic}'",
        )

        state.current_agent = AgentType.SEARCH
        state.workflow_status = WorkflowStatus.RUNNING

        total_sections = len(state.sections)
        for idx, section in enumerate(state.sections):
            self.logging_service.log(
                state=state,
                agent=AgentType.SEARCH,
                message=f"Searching for section [{idx + 1}/{total_sections}]: '{section.title}'",
            )
            section.status = TaskStatus.RUNNING

            # Delegate source selection entirely to SourceSelectionService
            source_type = self.source_selection_service.select_source(section)
            section.assigned_tool = source_type

            # Formulate query from topic and section title
            query = f"{state.topic} {section.title}".strip()
            request = ToolRequest(
                query=query,
                source=source_type,
            )

            # Delegate tool execution entirely to SearchService
            result = self.search_service.execute_search(request)
            section.research_results.append(result)

            # Update state.search_results dictionary for subsequent agents
            if section.title not in state.search_results:
                state.search_results[section.title] = []
            state.search_results[section.title].append(result)

            if result.success:
                section.status = TaskStatus.COMPLETED
            else:
                section.status = TaskStatus.FAILED
                self.logging_service.log(
                    state=state,
                    agent=AgentType.SEARCH,
                    message=f"Section '{section.title}' search failed: {result.error}",
                    level=LogLevel.WARNING,
                )

        state.progress = 35
        self.logging_service.log(
            state=state,
            agent=AgentType.SEARCH,
            message=f"Search phase completed for all {total_sections} sections.",
        )
        return state
