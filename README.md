# Твой Дизайн

Проект "Твой Дизайн" — это веб-сервис на базе Flask, который принимает данные через Webhooks и генерирует изображения на основе ответов пользователя.

## Структура проекта

```
your_design/
├── src/
│   ├── __init__.py
│   ├── app.py
│   └── image_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── test_image_generator.py
├── test_data.json
├── generated_images/
├── source_images/
│   ├── background/
│   │   └── default.png  # Пример фонового изображения
│   └── (другие папки с изображениями)
├── requirements.txt
└── venv/
```

## Установка

### Шаг 1: Клонирование репозитория

```bash
git clone git@github.com:sergeychernyakov/your_design.git
cd your_design
```

### Шаг 2: Создание виртуального окружения

```bash
python -m venv venv
```

### Шаг 3: Активация виртуального окружения

- На Windows:
  ```bash
  venv\Scripts\activate
  ```
- На macOS и Linux:
  ```bash
  source venv/bin/activate
  ```

### Шаг 4: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск приложения

### Шаг 1: Запуск Flask приложения

```bash
python src/app.py
```

### Шаг 2: Проверка статуса приложения

Откройте браузер и перейдите по адресу `http://localhost:5002`. Вы должны увидеть JSON сообщение:

```json
{
  "status": "Ok"
}
```

### Шаг 3: Установка и запуск ngrok

- Скачайте ngrok с [официального сайта](https://ngrok.com/) и установите его.
- Запустите ngrok, чтобы создать туннель к вашему локальному серверу (замените `5002` на порт вашего Flask-приложения, если он другой):

```bash
ngrok http 5002
```

- Скопируйте URL, который предоставляет ngrok (например, `http://abcd1234.ngrok.io`).

### Шаг 4: Настройка Webhook в квизе

1. Заходим в редактирование квиза из личного кабинета.
2. Заходим во вкладку «Интеграции» и выбираем Webhooks.
3. Добавляем хук и вписываем URL, предоставленный ngrok, добавив путь `/webhook`, например, `http://abcd1234.ngrok.io/webhook`.

## Тестирование

### Шаг 1: Запуск тестов с помощью unittest

```bash
python -m unittest discover tests
```

### Шаг 2: Отладка генерации изображения

Для отладки класса `ImageGenerator` используйте следующий шаг:

```bash
python -m src.image_generator
```

Это создаст изображение на основе данных в `test_data.json` и сохранит его в папке `generated_images`.

## Структура кода

**src/app.py** — Основной файл приложения Flask. Обрабатывает Webhook запросы и генерирует изображения на основе данных.

**src/image_generator.py** — Класс для генерации изображений на основе данных пользователя. Включает режим отладки.

**src/__init__.py** — Пустой файл для обозначения пакета.

**tests/test_app.py** — Файл с тестами для приложения. Включает тесты для проверки обработки Webhook запросов и генерации изображений.

**tests/test_image_generator.py** — Файл с тестами для класса `ImageGenerator`.

**test_data.json** — Файл с тестовыми данными для отладки класса `ImageGenerator`.

**generated_images/** — Папка для сохранения сгенерированных изображений.

**source_images/** — Папка для хранения фоновых изображений и других изображений.
