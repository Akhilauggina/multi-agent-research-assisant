from app.models.enums import AgentType, WorkflowStatus
from app.models.research_state import ResearchState
from app.services.fact_checking_service import FactCheckingService
from app.services.logging_service import LoggingService


class FactCheckerAgent:
    """
    Coordinates verification of read_results.
    Delegates validation to FactCheckingService.
    Produces verified_results: dict[str, str].
    """

    def __init__(
        self,
        fact_checking_service: FactCheckingService,
        logging_service: LoggingService | None = None,
    ) -> None:
        """
        Initializes FactCheckerAgent.

        Args:
            fact_checking_service: Injected FactCheckingService instance.
            logging_service: Injected LoggingService instance.
        """
        self.fact_checking_service = fact_checking_service
        self.logging_service = logging_service or LoggingService()

    def execute(self, state: ResearchState) -> ResearchState:
        """
        Validates and checks factual consistency for each section in read_results.

        Args:
            state: Active ResearchState.

        Returns:
            ResearchState: Updated state with verified_results populated.
        """
        self.logging_service.log(
            state=state,
            agent=AgentType.FACT_CHECKER,
            message=f"Starting fact-checking phase for topic: '{state.topic}'",
        )

        state.current_agent = AgentType.FACT_CHECKER
        state.workflow_status = WorkflowStatus.RUNNING

        for section_title, content in state.read_results.items():
            self.logging_service.log(
                state=state,
                agent=AgentType.FACT_CHECKER,
                message=f"Verifying factual integrity for section: '{section_title}'",
            )
            verified = self.fact_checking_service.verify_section(section_title, content)
            state.verified_results[section_title] = verified

        state.progress = 65
        self.logging_service.log(
            state=state,
            agent=AgentType.FACT_CHECKER,
            message=f"Fact-checking complete for {len(state.verified_results)} sections.",
        )
        return state

