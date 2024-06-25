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

### Настройка Ubuntu

1. Обновите пакеты и установите необходимые зависимости:

    ```bash
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip git tmux
    ```

2. Создайте нового пользователя (например, `webuser`):

    ```bash
    sudo adduser webuser
    sudo usermod -aG sudo webuser
    ```

3. Выйдите и войдите под новым пользователем:

    ```bash
    su - webuser
    ```

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/sergeychernyakov/your_design.git
cd your_design
```

### Шаг 2: Создание виртуального окружения

```bash
python3 -m venv venv
```

### Шаг 3: Активация виртуального окружения

- На macOS и Linux:
  ```bash
  source venv/bin/activate
  ```

### Шаг 4: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск приложения с использованием tmux

### Шаг 1: Запуск Flask приложения

1. Создайте новый сеанс `tmux`:

    ```bash
    tmux new -s flasksession
    ```

2. Внутри сеанса `tmux` запустите Flask приложение:

    ```bash
    cd ~/your_design
    source venv/bin/activate
    python app.py
    ```

3. Отсоединитесь от сеанса `tmux`, нажав `Ctrl + B`, затем `D`.

### Шаг 2: Запуск ngrok

1. В другом терминале подключитесь к серверу и создайте новый сеанс `tmux`:

    ```bash
    ssh webuser@89.111.175.202
    tmux new -s ngroksession
    ```

2. Внутри сеанса `tmux` запустите ngrok:

    ```bash
    ngrok http 5002
    ```

3. Отсоединитесь от сеанса `tmux`, нажав `Ctrl + B`, затем `D`.

### Шаг 3: Проверка статуса приложения

Взять активную ссылку можно здесь: https://dashboard.ngrok.com/cloud-edge/endpoints
Откройте браузер и перейдите по адресу, например, `https://5ddd-89-111-175-202.ngrok-free.app`. Вы должны увидеть JSON сообщение:

```json
{
  "status": "Ok"
}
```

### Шаг 4: Настройка Webhook в квизе

1. Заходим в редактирование квиза из личного кабинета.
2. Заходим во вкладку «Интеграции» и выбираем Webhooks.
3. Добавляем хук и вписываем URL, предоставленный ngrok, добавив путь `/webhook`, например, `https://5ddd-89-111-175-202.ngrok-free.app/webhook`.

## Управление сеансами tmux

### Подключение к сеансу tmux

Чтобы подключиться к уже запущенному сеансу `tmux`, выполните:

```bash
tmux attach -t flasksession  # для Flask приложения
tmux attach -t ngroksession  # для ngrok
```

### Список активных сеансов tmux

Чтобы увидеть список активных сеансов `tmux`, выполните:

```bash
tmux ls
```

### Завершение сеанса tmux

Чтобы завершить сеанс `tmux`, подключитесь к нему и завершите все запущенные процессы внутри сеанса, затем закройте сеанс:

```bash
tmux attach -t <session_name>
# внутри сеанса остановите процессы, затем закройте сеанс:
exit
```

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

