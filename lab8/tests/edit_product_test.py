import unittest
from api_client import APIClient, APIClientError, Product
from utils import load_test_config, find_product_by_id, compare_products

VALID_CONFIG_PATH = "../data/valid_data.json"
INVALID_CONFIG_PATH = "../data/invalid_data.json"


class EditProductTestCase(unittest.TestCase):
    def test_valid_edit_product(self):
        config = load_test_config(VALID_CONFIG_PATH)
        client = APIClient(config["base_url"])

        product_data = config["test_cases"]["valid_product_min_category_id"]
        setup_product = Product(**product_data)
        try:
            product_id = client.add_product(setup_product)
        except APIClientError as e:
            self.fail(f"Ошибка при создании тестового продукта: {e}")

        self.addCleanup(lambda: client.delete_product(product_id))

        for test_case_name, updated_product in config["test_cases"].items():
            with self.subTest(test_case_name):
                updated_product["id"] = product_id
                product = Product(**updated_product)
                try:
                    client.edit_product(product)
                except APIClientError as e:
                    self.fail(f"Ошибка при редактировании продукта: {e}")

                try:
                    updated_products = client.get_all_products()
                except APIClientError as e:
                    self.fail(f"Ошибка при получении списка продуктов: {e}")

                result_product = find_product_by_id(product_id, updated_products)
                self.assertIsNotNone(result_product, "Продукт не найден после редактирования")
                compare_products(self, product, result_product)

    def test_invalid_edit_product(self):
        invalid_config = load_test_config(INVALID_CONFIG_PATH)
        valid_config = load_test_config(VALID_CONFIG_PATH)

        client = APIClient(valid_config["base_url"])
        product_data = valid_config["test_cases"]["valid_product_min_category_id"]
        setup_product = Product(**product_data)

        try:
            product_id = client.add_product(setup_product)
        except APIClientError as e:
            self.fail(f"Ошибка при создании тестового продукта: {e}")

        self.addCleanup(lambda: client.delete_product(product_id))

        for test_case_name, invalid_product in invalid_config["test_cases"].items():
            with self.subTest(test_case_name):
                invalid_product["id"] = product_id
                product = Product(**invalid_product)
                with self.assertRaises(APIClientError) as context:
                    client.edit_product(product)
                self.assertIn("Bad request", str(context.exception), "Ожидалась ошибка BadRequest")

                try:
                    products = client.get_all_products()
                except APIClientError as e:
                    self.fail(f"Ошибка при получении списка продуктов: {e}")

                created_product = find_product_by_id(product_id, products)
                self.assertIsNotNone(created_product, "Продукт не должен быть удалён при невалидном редактировании")
                compare_products(self, setup_product, created_product)


if __name__ == '__main__':
    unittest.main()
