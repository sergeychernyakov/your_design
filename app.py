# src/app.py

from flask import Flask, request, jsonify, send_from_directory
import os
import logging
from src.image_generator import ImageGenerator

# Initialize Flask application
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the image generator
image_generator = ImageGenerator()

# Configuration
UPLOAD_FOLDER = 'generated_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

        # Generate image
        image_path = image_generator.generate_image(answers)
        image_filename = os.path.basename(image_path)

        # Return the path to the image or URL
        return jsonify({"image_url": f"/images/{image_filename}"})

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
