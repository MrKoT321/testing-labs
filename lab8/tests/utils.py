import json


def load_test_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_product_by_id(product_id, products):
    return next((p for p in products if p.id == product_id), None)


def transform_price_to_assert(product):
    product.price = float(product.price)


def compare_products(test_case, expected, actual):
    ignore_fields = {"id", "alias"}

    for field in expected.__dataclass_fields__:
        if field in ignore_fields:
            continue

        setattr(expected, field, handle_big_number(getattr(expected, field)))
        setattr(actual, field, handle_big_number(getattr(actual, field)))

        test_case.assertEqual(
            getattr(expected, field),
            getattr(actual, field),
            f"Mismatch in field: {field}"
        )


def handle_big_number(num_str: str) -> str:
    if num_str == "99999999999999999999999999999999999999":
        return "1e38"
    if num_str == "-99999999999999999999999999999999999999":
        return "-1e38"
    return num_str
