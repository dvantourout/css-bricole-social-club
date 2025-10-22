import requests
from idealo.schemas import TrendingQueries


class Client:
    def __init__(cls):
        cls.base_url = "https://cdn.idealo.com"

    def _get_trending_queries_url(cls, country: str) -> str:
        return f"{cls.base_url}/storage/assets/trending-searches/trending_searches_{country}.json"

    def get_trending_queries(cls, *, country: str = "fr_FR") -> TrendingQueries:
        url = cls._get_trending_queries_url(country)

        response = requests.get(url)
        response.raise_for_status()

        json_data = response.json()

        validated_data = TrendingQueries.model_validate(json_data)

        return validated_data
