from app.models.enums import AgentType, WorkflowStatus
from app.models.research_state import ResearchState
from app.services.logging_service import LoggingService
from app.services.planning_service import PlanningService


class PlannerAgent:
    """
    Coordinates planning stage of the research workflow.
    Delegates research section creation to PlanningService.
    Uses LoggingService for all logging needs.
    """

    def __init__(
        self,
        planning_service: PlanningService,
        logging_service: LoggingService | None = None,
    ) -> None:
        """
        Initializes PlannerAgent.

        Args:
            planning_service: Injected PlanningService instance.
            logging_service: Injected LoggingService instance.
        """
        self.planning_service = planning_service
        self.logging_service = logging_service or LoggingService()

    def execute(self, state: ResearchState) -> ResearchState:
        """
        Executes planning phase, populating plan and sections in ResearchState.

        Args:
            state: Active ResearchState.

        Returns:
            ResearchState: Updated state with sections, plan, and progress.
        """
        self.logging_service.log(
            state=state,
            agent=AgentType.PLANNER,
            message=f"Starting planning phase for topic: '{state.topic}'",
        )

        state.current_agent = AgentType.PLANNER
        state.workflow_status = WorkflowStatus.RUNNING

        sections = self.planning_service.generate_research_sections(state.topic)
        state.sections = sections
        state.plan = [s.title for s in sections]
        state.progress = 20

        self.logging_service.log(
            state=state,
            agent=AgentType.PLANNER,
            message=f"Planning complete. Generated {len(sections)} sections.",
        )
        return state
