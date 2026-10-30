from app.models.research_state import ResearchState
from app.workflow.container import create_workflow


def main() -> None:
    # Build complete multi-agent workflow using DI container
    workflow = create_workflow()

    # Create initial state
    initial_state = ResearchState(
        topic="Artificial Intelligence",
    )

    # Execute LangGraph workflow
    final_state = workflow.run(initial_state)

    print("\n" + "=" * 60)
    print("FINAL GENERATED RESEARCH REPORT:")
    print("=" * 60)
    print(final_state.report)
    print("=" * 60)
    print(f"Workflow Status: {final_state.workflow_status.value}")
    print(f"Total Logs: {len(final_state.logs)}")
    print(f"Progress: {final_state.progress}%")


if __name__ == "__main__":
    main()
