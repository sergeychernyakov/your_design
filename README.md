# Твой Дизайн

Проект "Твой Дизайн" — это веб-сервис на базе Flask, который принимает данные через Webhooks и генерирует изображения на основе ответов пользователя.

## Структура проекта

```
your_design/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── auth.py
│   ├── forms.py
│   ├── image_generator.py
│   └── models/
│       ├── __init__.py
│       ├── image.py
│       ├── quiz.py
│       └── user.py
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── test_image_generator.py
├── test_data.json
├── generated_images/
├── source_images/
│   ├── <quiz_id>/
│   │   ├── background/
│   │   │   └── 1.png  # Пример фонового изображения
│   │   └── (другие папки с изображениями)
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
    python src/app.py
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

## Админка

### Настройка админки с использованием Flask-Admin и HTTP Basic Authentication

Для настройки админки мы используем расширение Flask-Admin и защищаем её с помощью HTTP Basic Authentication.

#### Шаг 1: Добавление Flask-Admin в проект

1. Убедитесь, что Flask-Admin установлен в вашем виртуальном окружении. Если нет, установите его:

    ```bash
    pip install flask-admin
    ```

2. Добавьте файл `src/auth.py` для реализации HTTP Basic Authentication:

    ```python
    # src/auth.py

    from functools import wraps
    from flask import request, Response

    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        return username == 'admin' and password == 'secret'

    def authenticate():
        """Sends a 401 response that

 enables basic auth"""
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        return decorated
    ```

3. Настройка админки находится в файле `src/app.py`. Мы добавили админку для моделей User, Quiz и Image:

    ```python
    # app.py

    from flask import Flask, request, jsonify, send_from_directory
    import os
    import logging
    from flask_admin import Admin, AdminIndexView
    from flask_admin.contrib.sqla import ModelView
    from src.models import db, User, Quiz, Image
    from src.image_generator import ImageGenerator
    from src.auth import requires_auth

    # Initialize Flask application
    app = Flask(__name__)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Configuration
    UPLOAD_FOLDER = 'generated_images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    # Custom AdminIndexView with authentication
    class MyAdminIndexView(AdminIndexView):
        @requires_auth
        def index(self):
            return super(MyAdminIndexView, self).index()

    # Custom ModelView with authentication
    class MyModelView(ModelView):
        @requires_auth
        def is_accessible(self):
            return True

    # Admin setup
    admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Quiz, db.session))
    admin.add_view(MyModelView(Image, db.session))

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({"status": "Ok"})

    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            data = request.json

            logger.info(f"Received data: {data}")

            # Extract user responses
            answers = {item['q']: item['a'] for item in data['answers']}
            
            # Extract user contact information
            contact_info = data.get('contacts', {})
            phone_number = contact_info.get('phone', '')
            name = contact_info.get('name', '')
            email = contact_info.get('email', '')
            
            if not phone_number:
                raise ValueError("Phone number is missing or invalid.")

            quiz_id = data.get('quiz').get('id')
            quiz_name = data.get('quiz').get('name')
            created = data.get('created')

            # Save quiz info
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                quiz = Quiz(id=quiz_id, name=quiz_name, created=created)
                db.session.add(quiz)
                db.session.commit()

            # Save user info
            user = User.query.filter_by(phone=phone_number).first()
            if not user:
                user = User(name=name, email=email, phone=phone_number)
                db.session.add(user)
                db.session.commit()

            # Initialize the image generator
            image_generator = ImageGenerator(quiz_id=quiz_id)

            # Generate image
            image_path = image_generator.generate_image(answers, phone_number)
            image_filename = os.path.basename(image_path)

            # Save image info
            image = Image(quiz_id=quiz_id, user_id=user.id, image_path=image_path, phone_number=phone_number)
            db.session.add(image)
            db.session.commit()

            # Return the path to the image or URL
            return jsonify({"image_url": f"/images/{quiz_id}/{image_filename}"})

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return jsonify({"error": "An error occurred while processing the request"}), 500

    @app.route('/images/<quiz_id>/<filename>')
    def uploaded_file(quiz_id, filename):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], quiz_id), filename)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5002)
    ```

### Шаг 2: Доступ к админке

1. Запустите Flask приложение, как описано выше в разделе "Запуск Flask приложения".
2. Откройте браузер и перейдите по адресу `http://127.0.0.1:5002/admin`.
3. Введите имя пользователя и пароль, указанные в функции `check_auth` (например, `admin` и `secret`).

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

## Очистка папки с генерированными картинками на сервере

### Шаг 1: Подключение к серверу

```bash
ssh webuser@89.111.175.202
```

### Шаг 2: Очистка папки

Перейдите в директорию с проектом и выполните команду для удаления всех файлов в папке `generated_images`:

```bash
cd ~/your_design/generated_images
rm -f *
```

## Обновление картинок коллажа в source_images

### Шаг 1: Подготовка новых изображений

Подготовьте новые изображения и сохраните их в соответствующие папки в `source_images`. Каждая категория изображений должна быть в отдельной папке, например cabinet.

### Шаг 2: Замена изображений

Переместите новые изображения в нужные папки, заменяя старые:

```bash
cd ~/your_design/source_images/<категория>
# Замените существующие изображения новыми  (1-4).png (jpg)
cp /path/to/new/image.png 1.png
```

### Шаг 3: Перезапуск приложения

После обновления изображений перезапустите Flask приложение:

1. Подключитесь к сеансу `tmux` для Flask приложения:

    ```bash
    tmux attach -t flasksession
    ```

2. Остановите текущее приложение (если оно запущено) и перезапустите его:

    ```bash
    Ctrl + C  # остановка приложения
    source venv/bin/activate
    python app.py
    ```

## Скачивание получившегося изображения

После генерации изображения вы можете скачать его, следуя этим шагам:

1. Получите URL изображения, который возвращается в ответе на Webhook запрос. Например, если URL `https://5ddd-89-111-175-202.ngrok-free.app/images/<phone number>_1(2,3,4,5...).png`, например, https://5ddd-89-111-175-202.ngrok-free.app/images/79111234567_1.png.

2. Откройте этот URL в браузере. Изображение откроется в новом окне.

3. Нажмите правой кнопкой мыши на изображение и выберите "Сохранить изображение как..." для скачивания изображения на ваш локальный компьютер.

## Структура кода

**src/app.py** — Основной файл приложения Flask. Обрабатывает Webhook запросы и генерирует изображения на основе данных.

**src/image_generator.py** — Класс для генерации изображений на основе данных пользователя. Включает режим отладки.

**src/__init__.py** — Пустой файл для обозначения пакета.

**src/models/__init__.py** — Инициализация базы данных SQLAlchemy и импорт моделей.

**src/models/user.py** — Модель для хранения информации о пользователях.

**src/models/quiz.py** — Модель для хранения информации о квизах.

**src/models/image.py** — Модель для хранения информации о сгенерированных изображениях.

**src/auth.py** — Middleware для HTTP Basic Authentication.

**tests/test_app.py** — Файл с тестами для приложения. Включает тест

ы для проверки обработки Webhook запросов и генерации изображений.

**tests/test_image_generator.py** — Файл с тестами для класса `ImageGenerator`.

**test_data.json** — Файл с тестовыми данными для отладки класса `ImageGenerator`.

**generated_images/** — Папка для сохранения сгенерированных изображений.

**source_images/** — Папка для хранения фоновых изображений и других изображений.


сервер « Collage» с Ubuntu 24.04 LTS, IP-адрес 89.111.175.202
Доступ к серверу
Логин: root
Пароль: pYIDmyD9H0QzQJDi

ssh webuser@89.111.175.202
Логин: webuser
L:LKj[_)+p[oko67i

https://5ddd-89-111-175-202.ngrok-free.app/webhook


Вам нужно зарегистрироваться здесь: https://dashboard.ngrok.com/tunnels/authtokens
и сгенерировать новый authtoken и прислать его мне

https://5ddd-89-111-175-202.ngrok-free.app/images/79111234567_1.png


Скандинавский 
https://mrqz.me/66377f58f77e650026c3c7c0

Лофт 
https://mrqz.me/66a75a6e18108a0026d95d74

Минимализм 
https://mrqz.me/66a75aa95ac9fb00268cf1f8 

Неоклассик
https://mrqz.me/66a75abd17df430026dbf6a3 

Современный 
https://mrqz.me/66a75ad49f61830026a976a9
