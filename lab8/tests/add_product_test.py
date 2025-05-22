import unittest
from api_client import APIClient, APIClientError, Product
from utils import load_test_config, find_product_by_id, compare_products

VALID_CONFIG_PATH = "../data/valid_data.json"
INVALID_CONFIG_PATH = "../data/invalid_data.json"


class TestProductAPI(unittest.TestCase):

    def test_valid_add_product(self):
        config = load_test_config(VALID_CONFIG_PATH)
        client = APIClient(config["base_url"])

        for testcase_name, product_data in config["test_cases"].items():
            with self.subTest(testcase_name):
                product = Product(**product_data)

                try:
                    product_id = client.add_product(product)
                except Exception as e:
                    self.fail(f"Ошибка при добавлении продукта: {e}")

                try:
                    products = client.get_all_products()
                except Exception as e:
                    self.fail(f"Ошибка при получении списка продуктов: {e}")

                created_product = find_product_by_id(product_id, products)
                self.assertIsNotNone(created_product, "Продукт найден после добавления")

                # Cleanup
                self.addCleanup(lambda: client.delete_product(created_product.id))

                compare_products(self, product, created_product)

                self.assertNotEqual("0", created_product.id, "ID продукта не '0'")
                self.assertTrue(created_product.alias, "Alias продукта сгенерирован автоматически")

    def test_invalid_add_product(self):
        config = load_test_config(INVALID_CONFIG_PATH)
        client = APIClient(config["base_url"])

        for testcase_name, product_data in config["test_cases"].items():
            with self.subTest(testcase_name):
                product = Product(**product_data)

                with self.assertRaises(APIClientError, msg="Ожидалась ошибка BadRequest для невалидных данных"):
                    client.add_product(product)

                try:
                    products = client.get_all_products()
                except Exception as e:
                    self.fail(f"Ошибка при получении списка продуктов: {e}")

                created_product = find_product_by_id(product.id, products)

                if created_product:
                    try:
                        client.delete_product(created_product.id)
                    except Exception as e:
                        self.fail(f"Не удалось удалить тестовый продукт: {e}")


if __name__ == "__main__":
    unittest.main()
