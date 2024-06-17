from flask import Flask, request, jsonify
import os
from src.image_generator import ImageGenerator

app = Flask(__name__)

# Инициализация генератора изображений
image_generator = ImageGenerator()

@app.route('/')
def index():
    return jsonify({"status": "Application is running"})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    print("Полученные данные:", data)

    # Извлечение ответов пользователя
    answers = {item['q']: item['a'] for item in data['answers']}
    
    # Генерация изображения
    image_path = image_generator.generate_image(answers)
    
    # Возвращаем путь к изображению или URL
    return jsonify({"image_url": f"/{image_path}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
