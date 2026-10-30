from typing import Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.models.research_state import ResearchState
from app.workflow.container import create_workflow

router = APIRouter(prefix="/research", tags=["Research"])

# Workflow instance initialized via Dependency Injection container
workflow = create_workflow()


class ResearchRequest(BaseModel):
    """
    Request model for triggering a new multi-agent research workflow.
    """

    topic: str = Field(..., min_length=2, max_length=200, example="Artificial Intelligence in Healthcare")


class ResearchResponse(BaseModel):
    """
    Response model returning the final research state.
    """

    research_id: str
    topic: str
    workflow_status: str
    progress: int
    plan: list[str]
    read_results: dict[str, str]
    verified_results: dict[str, str]
    final_summary: str | None
    report: str | None
    logs_count: int


@router.post("/start", response_model=ResearchResponse, status_code=status.HTTP_200_OK)
def start_research(request: ResearchRequest) -> ResearchResponse:
    """
    Initiates the multi-agent research workflow using LangGraph.
    Flows through: Planner -> Search -> Reader -> FactChecker -> Summarizer -> Writer.
    """
    try:
        initial_state = ResearchState(topic=request.topic)
        final_state = workflow.run(initial_state)

        return ResearchResponse(
            research_id=str(final_state.research_id),
            topic=final_state.topic,
            workflow_status=final_state.workflow_status.value,
            progress=final_state.progress,
            plan=final_state.plan,
            read_results=final_state.read_results,
            verified_results=final_state.verified_results,
            final_summary=final_state.final_summary,
            report=final_state.report,
            logs_count=len(final_state.logs),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research workflow failed: {str(exc)}",
        ) from exc

