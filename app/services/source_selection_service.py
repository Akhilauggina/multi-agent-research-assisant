from app.models.enums import SourceType
from app.models.research_section import ResearchSection
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SourceSelectionService:
    """
    Service responsible for deciding which SourceType should be used
    for a given ResearchSection. Encapsulates source selection rules so
    agents remain clean coordinators.
    """

    def select_source(self, section: ResearchSection) -> SourceType:
        """
        Determines the appropriate source type for a research section.

        Args:
            section: ResearchSection to evaluate.

        Returns:
            SourceType: Selected source type.
        """
        title_lower = section.title.lower()
        desc_lower = section.description.lower()

        # Rule-based routing to support extensible source types
        if any(keyword in title_lower or keyword in desc_lower for keyword in ["paper", "academic", "arxiv", "theorem", "equation", "proof"]):
            selected = SourceType.ARXIV
        elif any(keyword in title_lower or keyword in desc_lower for keyword in ["video", "youtube", "tutorial", "lecture", "talk"]):
            selected = SourceType.YOUTUBE
        elif any(keyword in title_lower or keyword in desc_lower for keyword in ["news", "latest", "recent", "web"]):
            selected = SourceType.DUCKDUCKGO
        else:
            selected = SourceType.WIKIPEDIA

        logger.info(f"Selected source '{selected.value}' for section '{section.title}'")
        return selected

