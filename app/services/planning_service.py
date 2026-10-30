import json
import re
from app.models.enums import SourceType, TaskStatus
from app.models.research_section import ResearchSection
from app.services.llm_service import LLMService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PlanningService:
    """
    Service responsible for breaking a research topic down into structured sections.
    Delegates generation to LLMService.
    """

    def __init__(self, llm_service: LLMService) -> None:
        """
        Initializes PlanningService with an injected LLMService.

        Args:
            llm_service: Injected LLMService instance.
        """
        self.llm_service = llm_service

    def generate_research_sections(self, topic: str) -> list[ResearchSection]:
        """
        Generates research sections for a given topic using LLMService.

        Args:
            topic: Research topic to plan for.

        Returns:
            list[ResearchSection]: Generated research sections.
        """
        system_prompt = (
            "You are an expert research planner. Break down the user's research topic into "
            "3 to 5 logical sections. Respond strictly with a JSON array of objects, "
            'where each object has keys "title" (string) and "description" (string). '
            "Do not include markdown code fences or other commentary."
        )

        user_prompt = f"Topic: {topic}"

        logger.info(f"Generating research plan for topic: '{topic}'")
        raw_output = self.llm_service.generate(prompt=user_prompt, system_prompt=system_prompt)

        sections = self._parse_sections(raw_output, topic)
        logger.info(f"Successfully generated {len(sections)} sections for '{topic}'")
        return sections

    def _parse_sections(self, raw_output: str, fallback_topic: str) -> list[ResearchSection]:
        """
        Parses LLM output into ResearchSection instances with fallback handling.

        Args:
            raw_output: Text response from LLMService.
            fallback_topic: Topic used to create fallback sections if parsing fails.

        Returns:
            list[ResearchSection]: List of parsed sections.
        """
        cleaned = raw_output.strip()
        # Strip potential markdown formatting if returned
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                sections = []
                for item in parsed:
                    if isinstance(item, dict):
                        sections.append(
                            ResearchSection(
                                title=item.get("title", "Untitled Section"),
                                description=item.get("description", ""),
                                assigned_tool=SourceType.WIKIPEDIA,
                                status=TaskStatus.PENDING,
                            )
                        )
                if sections:
                    return sections
        except Exception as e:
            logger.warning(f"Could not parse LLM output as JSON array: {e}. Falling back to default plan.")

        # Fallback plan if output is not structured JSON
        return [
            ResearchSection(
                title=f"Introduction to {fallback_topic}",
                description=f"Core concepts, definitions, and origins of {fallback_topic}.",
                assigned_tool=SourceType.WIKIPEDIA,
                status=TaskStatus.PENDING,
            ),
            ResearchSection(
                title=f"Key Developments and Mechanisms in {fallback_topic}",
                description=f"Significant milestones, methodology, and workings of {fallback_topic}.",
                assigned_tool=SourceType.WIKIPEDIA,
                status=TaskStatus.PENDING,
            ),
            ResearchSection(
                title=f"Current Trends and Impact of {fallback_topic}",
                description=f"Modern state, challenges, and future trajectories for {fallback_topic}.",
                assigned_tool=SourceType.WIKIPEDIA,
                status=TaskStatus.PENDING,
            ),
        ]


    def generate_research_sections(self, topic: str) -> list[ResearchSection]:
        """
        Generates research sections for a given topic using LLMService.

        Args:
            topic: Research topic to plan for.

        Returns:
            list[ResearchSection]: Generated research sections.
        """
        system_prompt = (
            "You are an expert research planner. Break down the user's research topic into "
            "3 to 5 logical sections. Respond strictly with a JSON array of objects, "
            'where each object has keys "title" (string) and "description" (string). '
            "Do not include markdown code fences or other commentary."
        )

        user_prompt = f"Topic: {topic}"

        logger.info(f"Generating research plan for topic: '{topic}'")
        raw_output = self.llm_service.generate(prompt=user_prompt, system_prompt=system_prompt)

        sections = self._parse_sections(raw_output, topic)
        logger.info(f"Successfully generated {len(sections)} sections for '{topic}'")
        return sections

    def _parse_sections(self, raw_output: str, fallback_topic: str) -> list[ResearchSection]:
        """
        Parses LLM output into ResearchSection instances with fallback handling.

        Args:
            raw_output: Text response from LLMService.
            fallback_topic: Topic used to create fallback sections if parsing fails.

        Returns:
            list[ResearchSection]: List of parsed sections.
        """
        cleaned = raw_output.strip()
        # Strip potential markdown formatting if returned
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                sections = []
                for item in parsed:
                    if isinstance(item, dict):
                        sections.append(
                            ResearchSection(
                                title=item.get("title", "Untitled Section"),
                                description=item.get("description", ""),
                                assigned_tool=SourceType.WIKIPEDIA,
                                status=TaskStatus.PENDING,
                            )
                        )
                if sections:
                    return sections
        except Exception as e:
            logger.warning(f"Could not parse LLM output as JSON array: {e}. Falling back to default plan.")

        # Fallback plan if output is not structured JSON
        return [
            ResearchSection(
                title=f"Introduction to {fallback_topic}",
                description=f"Core concepts, definitions, and origins of {fallback_topic}.",
                assigned_tool=SourceType.WIKIPEDIA,
                status=TaskStatus.PENDING,
            ),
            ResearchSection(
                title=f"Key Developments and Mechanisms in {fallback_topic}",
                description=f"Significant milestones, methodology, and workings of {fallback_topic}.",
                assigned_tool=SourceType.WIKIPEDIA,
                status=TaskStatus.PENDING,
            ),
            ResearchSection(
                title=f"Current Trends and Impact of {fallback_topic}",
                description=f"Modern state, challenges, and future trajectories for {fallback_topic}.",
                assigned_tool=SourceType.WIKIPEDIA,
                status=TaskStatus.PENDING,
            ),
        ]
        self.llm_service = llm_service