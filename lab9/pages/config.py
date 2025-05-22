BASE_URL = "http://shop.qatl.ru"

LOGIN_URL = "/user/login"

PRODUCT_NAME_CASIO = "Casio MRP-700-1AVEF"
PRODUCT_NAME_ROYAL = "Royal London 20034-02"
PRODUCT_NAME_CITIZEN = "Citizen AT0696-59E"

PRODUCT_PAGE_URL = "/product/casio-mrp-700-1avef"
CATEGORY_PAGE_URL = "/category/women"
SEARCH_PAGE_URL = "/search?s=clock"

PRODUCT_URL = "/product/casio-mrp-700-1avef"

QUANTITY_PRODUCTS_ONE = "1"
QUANTITY_PRODUCTS_TEN = "10"


class OrderData:
    def __init__(self, login, password, name, email, address, note):
        self.login = login
        self.password = password
        self.name = name
        self.email = email
        self.address = address
        self.note = note


EXISTING_TO_ORDER_DATA = OrderData(
    login="login.test",
    password="qwerty123",
    name="Вито Скаллета",
    email="example@example.com",
    address="Йошкар-Ола, ул. Вознесенская, 110",
    note="note note note"
)


class ProductTestData:
    def __init__(self, id, name, price, url):
        self.id = id
        self.name = name
        self.price = price
        self.url = url


PRODUCT_CASIO = ProductTestData(
    id="1",
    name="Casio MRP-700-1AVEF",
    price="300",
    url="/product/casio-mrp-700-1avef"
)


class AuthTestData:
    def __init__(self, login, password):
        self.login = login
        self.password = password


def get_valid_login_data():
    return AuthTestData(login="login.test", password="qwerty123")


def get_invalid_login_data():
    return AuthTestData(login="login.test", password="qwerty1234")
