from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Папка для сохранения изображений
IMAGE_FOLDER = 'generated_images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Извлечение ответов пользователя
    responses = {item['q']: item['a'] for item in data['raw']}
    contacts = data['contacts']
    
    # Генерация изображения
    image_path = generate_image(responses)
    
    # Возвращаем путь к изображению или URL
    return jsonify({"image_url": f"/{image_path}"})

def generate_image(responses):
    # Определение фонового изображения на основе первого вопроса
    palette = responses.get('palette_question_id', 'default')
    background_image_path = f"backgrounds/{palette}.png"
    
    # Загрузка фонового изображения
    if not os.path.exists(background_image_path):
        background_image_path = "backgrounds/default.png"
    background = Image.open(background_image_path)
    
    # Создание объекта для рисования
    draw = ImageDraw.Draw(background)
    font = ImageFont.load_default()
    
    # Пример добавления текста на изображение
    for idx, (question_id, answer) in enumerate(responses.items()):
        text = f"{question_id}: {answer}"
        draw.text((10, 10 + idx * 20), text, font=font, fill="black")
    
    # Сохранение изображения
    image_filename = f"{responses.get('user_id', 'unknown')}.png"
    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    background.save(image_path)
    
    return image_path

if __name__ == '__main__':
    app.run(debug=True)
