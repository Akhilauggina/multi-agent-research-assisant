import json
import urllib.error
import urllib.parse
import urllib.request
from app.models.responses.wikipedia_response import WikipediaResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WikipediaClient:
    """
    Client for interacting with the Wikipedia REST and MediaWiki Action APIs.
    Communicates with external Wikipedia endpoints, parses raw responses,
    and returns strongly typed WikipediaResponse models.
    """

    def __init__(self, timeout: float = 15.0, user_agent: str = "MultiAgentResearchAssistant/1.0") -> None:
        """
        Initializes WikipediaClient.

        Args:
            timeout: HTTP request timeout in seconds.
            user_agent: Custom User-Agent header for Wikipedia API compliance.
        """
        self.timeout = timeout
        self.user_agent = user_agent
        self.rest_summary_endpoint = "https://en.wikipedia.org/api/rest_v1/page/summary"
        self.search_api_endpoint = "https://en.wikipedia.org/w/api.php"

    def search_and_get_summary(self, query: str) -> WikipediaResponse:
        """
        Searches Wikipedia for the query and returns the summary of the best matching page.

        Args:
            query: Topic or keyword to search.

        Returns:
            WikipediaResponse: Strongly typed Wikipedia response model.

        Raises:
            ValueError: If query is empty.
            RuntimeError: If Wikipedia lookup fails or no article is found.
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        clean_query = query.strip()
        logger.info(f"Searching Wikipedia for: '{clean_query}'")

        # First attempt: Direct summary fetch using REST API
        encoded_title = urllib.parse.quote(clean_query.replace(" ", "_"))
        url = f"{self.rest_summary_endpoint}/{encoded_title}"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent, "Accept": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return WikipediaResponse(
                    title=data.get("title", clean_query),
                    summary=data.get("extract", "No extract available."),
                    url=data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{encoded_title}"),
                )
        except urllib.error.HTTPError as e:
            if e.code == 404:
                logger.info(f"Exact title '{clean_query}' not found. Falling back to search API.")
                return self._search_fallback(clean_query)
            raise RuntimeError(f"Wikipedia API error ({e.code}): {e.reason}") from e
        except Exception as e:
            logger.warning(f"Direct summary request failed: {e}. Trying fallback search.")
            return self._search_fallback(clean_query)

    def _search_fallback(self, query: str) -> WikipediaResponse:
        """
        Performs an opensearch fallback when direct page summary lookup is ambiguous or missing.

        Args:
            query: Search query.

        Returns:
            WikipediaResponse: The top search match response.
        """
        params = urllib.parse.urlencode({
            "action": "opensearch",
            "search": query,
            "limit": "1",
            "namespace": "0",
            "format": "json",
        })
        url = f"{self.search_api_endpoint}?{params}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent, "Accept": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                # OpenSearch format: [query, [titles], [descriptions], [urls]]
                titles = data[1] if len(data) > 1 else []
                descriptions = data[2] if len(data) > 2 else []
                urls = data[3] if len(data) > 3 else []

                if titles and urls:
                    summary = descriptions[0] if descriptions and descriptions[0] else f"Wikipedia article on {titles[0]}."
                    return WikipediaResponse(
                        title=titles[0],
                        summary=summary,
                        url=urls[0],
                    )
        except Exception as e:
            logger.error(f"Fallback Wikipedia search failed: {e}")

        # Return minimal response if fallback did not find a page
        return WikipediaResponse(
            title=query,
            summary=f"No direct Wikipedia article found for '{query}'.",
            url=f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}",
        )

