import requests
from adstrong.schemas import ProductsInput
from database import SessionDep

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


def list_products(*, db_session: SessionDep, query: str) -> ProductsInput:
    url = f"https://search-api.adstrong.com/api/v1/search"
    params = {
        "q": query,
        # "m": 101,  # TODO: TBD
        "_crawler_bot": 0,
        "bsa": "datashake",
    }
    headers = {"X-Country": "fr"}

    response = requests.get(url=url, params=params, headers=headers)
    response.raise_for_status()

    json_data = response.json()

    validated_data = ProductsInput.model_validate(json_data, strict=False)

    return validated_data
