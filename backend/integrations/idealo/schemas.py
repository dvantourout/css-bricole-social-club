from pydantic import BaseModel, Field


class TrendingQuerySchema(BaseModel):
    query: str
    popularity: int
    percent_increase: int = Field(alias="percentIncrease")


class TrendingQueriesSchema(BaseModel):
    locale: str
    queries: list[TrendingQuerySchema]
