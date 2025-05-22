import requests
from typing import List
from dataclasses import dataclass
import json


class APIClientError(Exception):
    """Custom exception for API client errors."""
    pass


@dataclass
class Product:
    id: str = ""
    category_id: str = ""
    title: str = ""
    alias: str = ""
    content: str = ""
    price: str = ""
    old_price: str = ""
    status: str = ""
    keywords: str = ""
    description: str = ""
    hit: str = ""


@dataclass
class ProductAddedResponse:
    id: int
    status: int


@dataclass
class ProductDeletedResponse:
    status: int


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_products(self) -> List[Product]:
        url = f"{self.base_url}/api/products"
        response = requests.get(url)
        if response.status_code != 200:
            raise APIClientError(f"Unexpected status code: {response.status_code}")

        try:
            return [Product(**self.filter_product_fields(prod)) for prod in json.loads(response.text)]
        except Exception as e:
            raise APIClientError(f"Failed to parse products: {e}, raw response: {response.text}")

    def add_product(self, product: Product) -> str:
        url = f"{self.base_url}/api/addproduct"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(product.__dict__))

        if response.status_code != 200:
            raise APIClientError(f"Unexpected status code: {response.status_code}")

        if self._check_on_error(response.text):
            raise APIClientError("Bad request detected in HTML")

        try:
            data = response.json()
            return str(data['id'])
        except Exception as e:
            raise APIClientError(f"Failed to parse response: {e}, raw response: {response.text}")

    def edit_product(self, product: Product) -> None:
        url = f"{self.base_url}/api/editproduct"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(product.__dict__))

        if response.status_code != 200:
            raise APIClientError(f"Unexpected status code: {response.status_code}, body: {response.text}")

        if self._check_on_error(response.text):
            raise APIClientError("Bad request detected in HTML")

    def delete_product(self, product_id: str) -> int:
        url = f"{self.base_url}/api/deleteproduct?id={product_id}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIClientError(f"Unexpected status code: {response.status_code}")

        if self._check_on_error(response.text):
            raise APIClientError("Bad request detected in HTML")

        try:
            data = response.json()
            return data['status']
        except Exception as e:
            raise APIClientError(f"Failed to parse response: {e}, raw response: {response.text}")

    @staticmethod
    def filter_product_fields(data: dict) -> dict:
        allowed_fields = {field.name for field in Product.__dataclass_fields__.values()}
        return {k: v for k, v in data.items() if k in allowed_fields}

    def _check_on_error(self, body: str) -> bool:
        return "<h1>Произошла ошибка</h1>" in body
