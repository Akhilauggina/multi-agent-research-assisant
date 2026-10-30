from app.models.enums import AgentType, WorkflowStatus
from app.models.research_state import ResearchState
from app.services.logging_service import LoggingService
from app.services.writer_service import WriterService


class WriterAgent:
    """
    Coordinates creation of the final research report.
    Delegates report authoring to WriterService.
    Produces report: str (strictly Markdown).
    """

    def __init__(
        self,
        writer_service: WriterService,
        logging_service: LoggingService | None = None,
    ) -> None:
        """
        Initializes WriterAgent.

        Args:
            writer_service: Injected WriterService instance.
            logging_service: Injected LoggingService instance.
        """
        self.writer_service = writer_service
        self.logging_service = logging_service or LoggingService()

    def execute(self, state: ResearchState) -> ResearchState:
        """
        Generates markdown report based on final_summary and verified_results.

        Args:
            state: Active ResearchState.

        Returns:
            ResearchState: Updated state with report populated and completed status.
        """
        self.logging_service.log(
            state=state,
            agent=AgentType.WRITER,
            message=f"Starting report generation for topic: '{state.topic}'",
        )

        state.current_agent = AgentType.WRITER
        state.workflow_status = WorkflowStatus.RUNNING

        report = self.writer_service.generate_report(
            topic=state.topic,
            final_summary=state.final_summary or "",
            verified_results=state.verified_results,
        )

        state.report = report
        state.progress = 100
        state.workflow_status = WorkflowStatus.COMPLETED

        self.logging_service.log(
            state=state,
            agent=AgentType.WRITER,
            message="Report generation completed successfully. Research workflow finished.",
        )
        return state

