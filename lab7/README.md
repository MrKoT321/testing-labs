## Лабораторная работа №7

* Для Mock-сервиса используется Mountebank
* Чтобы имитировать Api запрос следует загрузить `currency_mock.json`
* Для загрузки можно использовать curl:

```bash
curl -X POST http://localhost:2525/imposters  -H "Content-Type: application/json" -d @currency_mock.json
```