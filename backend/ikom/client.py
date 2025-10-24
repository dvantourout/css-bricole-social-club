import json
import logging

import requests
from bs4 import BeautifulSoup
from ikom.schemas import ProductInput
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class Client:
    def __init__(self):
        self.base_url = "https://www.ikom-shopping.com/fr-fr/ajax/results"

    def list_products(self, *, query: str) -> list[ProductInput]:
        url = self.base_url

        params = {
            "page": 1,
            "query": query,
            "categId": None,
            "categLabel": None,
            "brandLabel": None,
            "merchantLabel": None,
            "merchantDomainLabel": None,
            "categFilt": None,
            "selectedMinPrice": 0,
            "selectedMaxPrice": None,
            "initialMinPrice": None,
            "initialMaxPrice": None,
            "limit": 100,  # 100
            "sort": "popularity",
            "skip": 0,
        }

        response = requests.get(
            url=url,
            params=params,
        )
        response.raise_for_status()

        html_content = response.text
        soup = BeautifulSoup(html_content)

        elements_with_data_json = soup.find_all(attrs={"data-json": True})

        products: list[ProductInput] = []

        for element in elements_with_data_json:
            data_json = element.get("data-json")
            # products_json = (json.loads(data_json))

            try:
                products.append(ProductInput.model_validate_json(data_json))
            except ValidationError as e:
                logger.error(json.loads(data_json))

        return products
