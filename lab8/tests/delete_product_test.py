import unittest
from api_client import APIClient, APIClientError, Product
from utils import load_test_config, find_product_by_id

VALID_CONFIG_PATH = "../data/valid_data.json"


class DeleteProductTestCase(unittest.TestCase):
    def test_delete_product(self):
        config = load_test_config(VALID_CONFIG_PATH)
        client = APIClient(config["base_url"])

        product_data = config["test_cases"]["valid_product_min_category_id"]
        product = Product(**product_data)

        try:
            product_id = client.add_product(product)
        except APIClientError as e:
            self.fail(f"Не удалось создать продукт для теста: {e}")

        try:
            created_products = client.get_all_products()
        except APIClientError as e:
            self.fail(f"Не удалось получить список продуктов после добавления: {e}")

        created_product = find_product_by_id(product_id, created_products)
        self.assertIsNotNone(created_product, "Созданный продукт не найден в списке продуктов")

        with self.subTest("Delete existing product"):
            try:
                status = client.delete_product(created_product.id)
            except APIClientError as e:
                self.fail(f"Ошибка при удалении существующего продукта: {e}")
            self.assertEqual(status, 1, "Статус удаления существующего продукта должен быть 1")

            try:
                products = client.get_all_products()
            except APIClientError as e:
                self.fail(f"Не удалось получить список продуктов после удаления: {e}")

            found = any(p.id == created_product.id for p in products)
            self.assertFalse(found, "Продукт всё ещё существует после удаления")

        with self.subTest("Delete non-existing product"):
            try:
                status = client.delete_product("-999999")
            except APIClientError as e:
                self.fail(f"Ошибка при попытке удалить несуществующий продукт: {e}")
            self.assertEqual(status, 0, "Статус удаления несуществующего продукта должен быть 0")


if __name__ == '__main__':
    unittest.main()
