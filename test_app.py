import pytest
from app import app
from src.image_generator import ImageGenerator
import json
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_webhook(client):
    # Пример данных для тестирования
    test_data = {
        "raw": [
            {"q": "palette_question_id", "a": "blue_palette"},
            {"q": "question_2", "a": "answer_2"},
            {"q": "question_3", "a": "answer_3"}
        ],
        "contacts": {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890"
        }
    }
    
    response = client.post('/webhook', data=json.dumps(test_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert "image_url" in data

    # Проверка, что изображение создано
    image_path = data['image_url'].lstrip('/')
    assert os.path.exists(image_path)

    # Удаление тестового изображения после проверки
    if os.path.exists(image_path):
        os.remove(image_path)

def test_generate_image():
    generator = ImageGenerator()
    
    responses = {
        "palette_question_id": "blue_palette",
        "question_2": "answer_2",
        "question_3": "answer_3",
        "user_id": "test_user"
    }
    
    image_path = generator.generate_image(responses)
    assert os.path.exists(image_path)

    # Удаление тестового изображения после проверки
    if os.path.exists(image_path):
        os.remove(image_path)
