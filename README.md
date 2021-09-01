# task
## Необходимые шаги для инсталляции:
1. python3 -m venv venv
2. . venv/bin/activate
3. pip install -r requirements.txt
## Команды для запуска сервиса:
1. docker run -d -p 27017:27017 mongo)
2. python main.py
## curl команды с нужными параметрами для прохождения тестового сценария:
### Создание товаров
  1. curl --header "Content-Type: application/json" -X POST -d '{"title": "IPhone 42", "description": "coolest phone", "height": 65, "widht": 21}' http://localhost:8080/create_item
  2. curl --header "Content-Type: application/json" -X POST -d '{"title": "Somephone", "description": "not cool", "height": 35, "widht": 21}' http://localhost:8080/create_item
  3. curl --header "Content-Type: application/json" -X POST -d '{"title": "laptop", "description": "cool enough", "quality": 10}' http://localhost:8080/create_item
  4. curl --header "Content-Type: application/json" -X POST -d '{"title": "Jon Snow", "description": "knows nothing", "height": 175, "widht": 95}' http://localhost:8080/create_item
### Получить информацию о всех товарах
  1. curl --header "Content-Type: application/json" -X GET http://localhost:8080/get_items
### Получить названия товаров в отсортированном по одному из полей порядке
  1. Например: curl --header "Content-Type: application/json" -X GET -d '{"sort": "height"}' http://localhost:8080/get_items
### Найти товары по выбранному параметру и его значению
  1. Например: curl --header "Content-Type: application/json" -X GET -d '{"widht": 21}' http://localhost:8080/get_filter
### Получить детали товара по ID
  1. Например: curl --header "Content-Type: application/json" -X GET -d '{"\_id": "612f6bd43177708f3130e28a"}' http://localhost:8080/get_item
  2. Узнать \_id товаров можно из пункта 2.
