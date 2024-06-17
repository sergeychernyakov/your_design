from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import json
import uuid

class ImageGenerator:
    def __init__(self, backgrounds_folder='source_images/background', output_folder='generated_images'):
        self.backgrounds_folder = backgrounds_folder
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
    
    def find_image_path(self, folder, palette, answer):
        """
        Finds the path of the image based on the folder, palette, and answer.
        """
        palette_folder = os.path.join('source_images', folder, palette)
        if os.path.exists(palette_folder):
            image_path_png = os.path.join(palette_folder, f"{answer}.png")
            image_path_jpg = os.path.join(palette_folder, f"{answer}.jpg")
        else:
            image_path_png = os.path.join('source_images', folder, f"{answer}.png")
            image_path_jpg = os.path.join('source_images', folder, f"{answer}.jpg")

        if os.path.exists(image_path_png):
            return image_path_png
        elif os.path.exists(image_path_jpg):
            return image_path_jpg
        return None
    
    def generate_image(self, responses):
        """
        Generates an image collage based on the given responses.
        """
        question_to_folder = {
            "Выберите Палитру": "palette",
            "Выберите Керамогранит": "porcelain",
            "Выберите Пол": "floor",
            "Выберите Свет": "light",
            "Выберите Тумбу": "cabinet",
            "Выберите Душ": "shower",
            "Выберите Дверь": "door",
            "Выберите Кухню": "kitchen",
            "Выберите Диван": "sofa",
            "Выберите Стул": "chair",
            "Выберите Шторы": "curtain",
            "Выберите Подушку": "pillow"
        }

        elements_positions = {
            "Выберите Палитру": (625, 900, 415),    
            "Выберите Керамогранит": (250, 710, 360),
            "Выберите Пол": (490, 420, 350),   
            "Выберите Свет": (320, 40, 250),   
            "Выберите Тумбу": (80, 610, 250),  
            "Выберите Душ": (380, 580, 200),
            "Выберите Кухню": (600, 95, 430),
            "Выберите Дверь": (870, 360, 180),
            "Выберите Диван": (40, 340, 560),
            "Выберите Стул": (690, 596, 300),  
            "Выберите Шторы": (100, 40, 200),  
            "Выберите Подушку": (360, 350, 130)   
        }

        layer_order = [
            "Выберите Палитру",
            "Выберите Пол",
            "Выберите Керамогранит",
            "Выберите Тумбу",
            "Выберите Душ",
            "Выберите Кухню",
            "Выберите Дверь",
            "Выберите Шторы",
            "Выберите Диван",
            "Выберите Стул",
            "Выберите Подушку",
            "Выберите Свет"
        ]

        palette = responses.get("Выберите Палитру", "1")
        background_image_path = os.path.join(self.backgrounds_folder, f"{palette}.png")
        if not os.path.exists(background_image_path):
            raise FileNotFoundError(f"Background image not found for palette {palette}.")
        
        background = Image.open(background_image_path).convert("RGBA")
        collage = Image.new('RGBA', background.size, (255, 255, 255, 0))
        collage.paste(background, (0, 0))

        for question in layer_order:
            if question not in responses:
                continue

            answer = responses[question]
            folder = question_to_folder.get(question, "default")
            image_path = self.find_image_path(folder, palette, answer)
            if not image_path:
                print(f"Image for {answer} in folder {folder} does not exist")
                continue

            image = Image.open(image_path).convert("RGBA")
            x, y, width = elements_positions[question]
            image.thumbnail((width, image.height), Image.LANCZOS)
            paste_position = (x, y)
            collage.paste(image, paste_position, image)

        collage = collage.convert("RGB")
        unique_filename = f"generated_image_{uuid.uuid4()}.png"
        image_path = os.path.join(self.output_folder, unique_filename)
        collage.save(image_path)
        
        return image_path

def main():
    with open('test_data.json', 'r') as file:
        test_data = json.load(file)["answers"]
    
    test_data_dict = {item['q']: item['a'] for item in test_data}
    
    generator = ImageGenerator()
    
    image_path = generator.generate_image(test_data_dict)
    print(f"Image saved at: {image_path}")

if __name__ == '__main__':
    main()
