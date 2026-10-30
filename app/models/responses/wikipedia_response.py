from pydantic import BaseModel, ConfigDict, HttpUrl


class WikipediaResponse(BaseModel):
    """
    Response model representing parsed Wikipedia article data.
    """

    model_config = ConfigDict(frozen=True)

    title: str
    summary: str
    url: str

