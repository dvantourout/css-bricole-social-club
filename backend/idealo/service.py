import requests
from database import SessionDep
from idealo.schemas import TrendingQueries


def list_trending_queries(
    *, db_session: SessionDep, country: str = "fr_FR"
) -> TrendingQueries:
    url = f"https://cdn.idealo.com/storage/assets/trending-searches/trending_searches_{country}.json"

    response = requests.get(url)
    response.raise_for_status()

    json_data = response.json()

    validated_data = TrendingQueries.model_validate(json_data)

    return validated_data
