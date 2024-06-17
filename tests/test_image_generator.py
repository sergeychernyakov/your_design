import unittest
import os
from PIL import Image
from src.image_generator import ImageGenerator

class TestImageGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.image_generator = ImageGenerator(
            backgrounds_folder='source_images/background',
            output_folder='generated_images'
        )
        cls.responses = {
            "Выберите Палитру": "1",
            "Выберите Керамогранит": "2",
            "Выберите Пол": "3",
            "Выберите Свет": "4",
            "Выберите Тумбу": "1",
            "Выберите Душ": "2",
            "Выберите Дверь": "3",
            "Выберите Кухню": "4",
            "Выберите Диван": "1",
            "Выберите Стул": "2",
            "Выберите Шторы": "3",
            "Выберите Подушку": "4"
        }

    def test_find_image_path(self):
        folder = "sofa"
        palette = "1"
        answer = "1"
        image_path = self.image_generator.find_image_path(folder, palette, answer)
        expected_path = os.path.join('source_images', folder, palette, f"{answer}.png")
        self.assertEqual(image_path, expected_path)

    def test_generate_image(self):
        image_path = self.image_generator.generate_image(self.responses)
        self.assertTrue(os.path.exists(image_path))

        # Verify that the generated image is a valid image file
        with Image.open(image_path) as img:
            self.assertTrue(img.format, 'PNG')

    @classmethod
    def tearDownClass(cls):
        # Clean up generated images
        for file in os.listdir(cls.image_generator.output_folder):
            file_path = os.path.join(cls.image_generator.output_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    unittest.main()
