from app.models.enums import AgentType, WorkflowStatus
from app.models.research_state import ResearchState
from app.services.logging_service import LoggingService
from app.services.summarization_service import SummarizationService


class SummarizerAgent:
    """
    Coordinates summarization of verified_results.
    Delegates combination and synthesis to SummarizationService.
    Produces final_summary: str.
    Does NOT generate markdown or reports.
    """

    def __init__(
        self,
        summarization_service: SummarizationService,
        logging_service: LoggingService | None = None,
    ) -> None:
        """
        Initializes SummarizerAgent.

        Args:
            summarization_service: Injected SummarizationService instance.
            logging_service: Injected LoggingService instance.
        """
        self.summarization_service = summarization_service
        self.logging_service = logging_service or LoggingService()

    def execute(self, state: ResearchState) -> ResearchState:
        """
        Combines verified sections into a single concise final_summary.

        Args:
            state: Active ResearchState.

        Returns:
            ResearchState: Updated state with final_summary populated.
        """
        self.logging_service.log(
            state=state,
            agent=AgentType.SUMMARIZER,
            message=f"Starting summarization phase for topic: '{state.topic}'",
        )

        state.current_agent = AgentType.SUMMARIZER
        state.workflow_status = WorkflowStatus.RUNNING

        summary = self.summarization_service.summarize_results(
            topic=state.topic,
            verified_results=state.verified_results,
        )
        state.final_summary = summary
        state.progress = 80

        self.logging_service.log(
            state=state,
            agent=AgentType.SUMMARIZER,
            message="Summarization phase completed successfully.",
        )
        return state

