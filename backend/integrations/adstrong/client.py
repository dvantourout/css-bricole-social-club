import requests
from integrations.adstrong.schemas import AdstrongProductsSchema, ProductInputSchema

# q: chaussures securite timberland
# page: 1
# fcb: 0
# excludedSellers:
# freeShipping: 0
# conditions: ALL
# m: 101
# _crawler_bot: 0
# returnShops: 0
# bsa: datashake


class AdstrongClient:
    def __init__(cls):
        cls.base_url = "https://search-api.adstrong.com"

    def get_api_url(cls) -> str:
        return f"{cls.base_url}/api/v1/search"

    def list_products(cls, *, query: str) -> list[ProductInputSchema]:
        url = cls.get_api_url()

        params = {
            "q": query,
            "m": 101,  # TODO: TBD
            "_crawler_bot": 0,
            "bsa": "datashake",
            "conditions": "NEW",
        }
        headers = {"X-Country": "fr"}

        response = requests.get(
            url=url,
            params=params,
            headers=headers,
        )
        response.raise_for_status()

        json_data = response.json()

        validated_data = AdstrongProductsSchema.model_validate(json_data, strict=False)

        return validated_data.products
