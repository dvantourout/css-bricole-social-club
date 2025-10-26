import requests
from integrations.idealo.schemas import TrendingQueriesSchema


class Client:
    def __init__(cls):
        cls.base_url = "https://cdn.idealo.com"

    def _get_trending_queries_url(cls, locale: str) -> str:
        return f"{cls.base_url}/storage/assets/trending-searches/trending_searches_{locale}.json"

    def get_trending_queries(cls, *, locale: str = "fr_FR") -> TrendingQueriesSchema:
        url = cls._get_trending_queries_url(locale)

        response = requests.get(url)
        response.raise_for_status()

        json_data = response.json()

        validated_data = TrendingQueriesSchema.model_validate(json_data)

        return validated_data
