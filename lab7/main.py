import requests


def get_currency_rates(base="USD"):
    url = "http://localhost:4545/api/rates"
    params = {"base": base}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Курс валют для {base}:")
        for currency, rate in data["rates"].items():
            print(f"  {currency}: {rate}")
    else:
        print(f"Ошибка: {response.status_code}")


if __name__ == "__main__":
    get_currency_rates()
    get_currency_rates("EUR")
    get_currency_rates("GBP")
    get_currency_rates("JPY")
