from pydantic import BaseModel, Field


class TrendingQuery(BaseModel):
    query: str
    popularity: int
    percent_increase: int = Field(alias="percentIncrease")


class TrendingQueries(BaseModel):
    locale: str
    queries: list[TrendingQuery]
