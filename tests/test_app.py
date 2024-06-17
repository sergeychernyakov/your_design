import unittest
import json
import os
from flask import Flask
from app import app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

        cls.sample_data = {
            "answers": [
                {"q": "Выберите Палитру", "t": "images", "a": "1"},
                {"q": "Выберите Керамогранит", "t": "images", "a": "2"},
                {"q": "Выберите Пол", "t": "images", "a": "2"},
                {"q": "Выберите Свет", "t": "images", "a": "2"},
                {"q": "Выберите Тумбу", "t": "images", "a": "2"},
                {"q": "Выберите Душ", "t": "images", "a": "2"},
                {"q": "Выберите Дверь", "t": "images", "a": "2"},
                {"q": "Выберите Кухню", "t": "images", "a": "2"},
                {"q": "Выберите Диван", "t": "images", "a": "2"},
                {"q": "Выберите Стул", "t": "images", "a": "2"},
                {"q": "Выберите Шторы", "t": "images", "a": "1"},
                {"q": "Выберите Подушку", "t": "images", "a": "2"}
            ]
        }

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "Ok"})

    def test_webhook(self):
        response = self.client.post('/webhook', data=json.dumps(self.sample_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("image_url", response.json)

        # Check if the generated image exists
        image_url = response.json["image_url"]
        image_filename = os.path.basename(image_url)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        self.assertTrue(os.path.exists(image_path))

    def test_uploaded_file(self):
        response = self.client.post('/webhook', data=json.dumps(self.sample_data), content_type='application/json')
        image_url = response.json["image_url"]
        image_filename = os.path.basename(image_url)

        response = self.client.get(f'/images/{image_filename}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')

    @classmethod
    def tearDownClass(cls):
        # Clean up generated images
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    unittest.main()
