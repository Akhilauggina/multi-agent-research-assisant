from typing import Any
from langgraph.graph import StateGraph, START, END
from app.agents.fact_checker_agent import FactCheckerAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.reader_agent import ReaderAgent
from app.agents.search_agent import SearchAgent
from app.agents.summarizer_agent import SummarizerAgent
from app.agents.writer_agent import WriterAgent
from app.models.research_state import ResearchState


class ResearchWorkflow:
    """
    LangGraph-based state machine orchestrating the multi-agent research workflow.
    Each agent acts as an independent node executing sequentially:
    START -> Planner -> Search -> Reader -> FactChecker -> Summarizer -> Writer -> END.
    """

    def __init__(
        self,
        planner_agent: PlannerAgent,
        search_agent: SearchAgent,
        reader_agent: ReaderAgent,
        fact_checker_agent: FactCheckerAgent,
        summarizer_agent: SummarizerAgent,
        writer_agent: WriterAgent,
    ) -> None:
        """
        Initializes the research workflow graph with injected agents.

        Args:
            planner_agent: PlannerAgent node.
            search_agent: SearchAgent node.
            reader_agent: ReaderAgent node.
            fact_checker_agent: FactCheckerAgent node.
            summarizer_agent: SummarizerAgent node.
            writer_agent: WriterAgent node.
        """
        self.planner_agent = planner_agent
        self.search_agent = search_agent
        self.reader_agent = reader_agent
        self.fact_checker_agent = fact_checker_agent
        self.summarizer_agent = summarizer_agent
        self.writer_agent = writer_agent

        self.graph = self._build_graph()

    def _build_graph(self) -> Any:
        """
        Assembles and compiles the LangGraph StateGraph.

        Returns:
            CompiledStateGraph: Compiled LangGraph executable.
        """
        workflow = StateGraph(ResearchState)

        # Register agent nodes
        def plan_node(state: ResearchState) -> ResearchState:
            return self.planner_agent.execute(state)

        def search_node(state: ResearchState) -> ResearchState:
            return self.search_agent.execute(state)

        def read_node(state: ResearchState) -> ResearchState:
            return self.reader_agent.execute(state)

        def fact_check_node(state: ResearchState) -> ResearchState:
            return self.fact_checker_agent.execute(state)

        def summarize_node(state: ResearchState) -> ResearchState:
            return self.summarizer_agent.execute(state)

        def write_node(state: ResearchState) -> ResearchState:
            return self.writer_agent.execute(state)

        workflow.add_node("planner", plan_node)
        workflow.add_node("search", search_node)
        workflow.add_node("reader", read_node)
        workflow.add_node("fact_checker", fact_check_node)
        workflow.add_node("summarizer", summarize_node)
        workflow.add_node("writer", write_node)

        # Wire sequential pipeline
        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "search")
        workflow.add_edge("search", "reader")
        workflow.add_edge("reader", "fact_checker")
        workflow.add_edge("fact_checker", "summarizer")
        workflow.add_edge("summarizer", "writer")
        workflow.add_edge("writer", END)

        return workflow.compile()

    def run(self, initial_state: ResearchState) -> ResearchState:
        """
        Executes the compiled LangGraph workflow from start to finish.

        Args:
            initial_state: Initial ResearchState with topic populated.

        Returns:
            ResearchState: Fully processed research state after writer node completes.
        """
        output = self.graph.invoke(initial_state)
        if isinstance(output, ResearchState):
            return output
        # If LangGraph returns a dictionary representation, validate back into ResearchState
        return ResearchState.model_validate(output)

