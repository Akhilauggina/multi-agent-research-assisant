from app.models.enums import AgentType, WorkflowStatus
from app.models.research_state import ResearchState
from app.services.logging_service import LoggingService
from app.services.reader_service import ReaderService


class ReaderAgent:
    """
    Coordinates processing of search_results across research sections.
    Delegates extraction to ReaderService.
    Produces read_results: dict[str, str].
    Does NOT summarize or verify facts.
    """

    def __init__(
        self,
        reader_service: ReaderService,
        logging_service: LoggingService | None = None,
    ) -> None:
        """
        Initializes ReaderAgent.

        Args:
            reader_service: Injected ReaderService instance.
            logging_service: Injected LoggingService instance.
        """
        self.reader_service = reader_service
        self.logging_service = logging_service or LoggingService()

    def execute(self, state: ResearchState) -> ResearchState:
        """
        Reads and extracts factual content section by section from search_results.

        Args:
            state: Active ResearchState.

        Returns:
            ResearchState: Updated state with read_results populated.
        """
        self.logging_service.log(
            state=state,
            agent=AgentType.READER,
            message=f"Starting reader phase for topic: '{state.topic}'",
        )

        state.current_agent = AgentType.READER
        state.workflow_status = WorkflowStatus.RUNNING

        # Process each section present in search_results (or state.sections)
        for section_title, tool_results in state.search_results.items():
            self.logging_service.log(
                state=state,
                agent=AgentType.READER,
                message=f"Extracting content for section: '{section_title}'",
            )
            extracted = self.reader_service.read_and_extract(section_title, tool_results)
            state.read_results[section_title] = extracted

        # Handle any planned sections that didn't appear in search_results
        for section in state.sections:
            if section.title not in state.read_results:
                extracted = self.reader_service.read_and_extract(section.title, section.research_results)
                state.read_results[section.title] = extracted

        state.progress = 50
        self.logging_service.log(
            state=state,
            agent=AgentType.READER,
            message=f"Reader phase complete. Processed {len(state.read_results)} sections.",
        )
        return state

