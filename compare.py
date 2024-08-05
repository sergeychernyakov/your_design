# src/app.py

from flask import Flask, request, jsonify, send_from_directory, url_for, render_template_string
import os
import logging
import io
import base64
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from sqlalchemy.orm import joinedload
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for rendering to files
import matplotlib.pyplot as plt
from src.models.user import db, User
from src.models.quiz import Quiz
from src.models.image import Image
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

# Custom AdminIndexView with pie chart and additional data
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @requires_auth
    def index(self):
        # Generate pie chart
        quizzes = db.session.query(Quiz).all()
        quiz_names = [quiz.name for quiz in quizzes]
        quiz_counts = [db.session.query(Image).filter_by(quiz_id=quiz.id).count() for quiz in quizzes]

        fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted size for better layout
        wedges, texts, autotexts = ax.pie(quiz_counts, labels=quiz_names, autopct='%1.1f%%', startangle=140, textprops=dict(color="w"))

        # Improve label spacing
        plt.setp(autotexts, size=10, weight="bold")
        ax.legend(wedges, quiz_names, title="Quizzes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the pie chart to a bytes object
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches="tight")  # bbox_inches="tight" to ensure nothing is cut off
        img.seek(0)
        chart_data = base64.b64encode(img.getvalue()).decode()

        # Get additional data
        total_users = db.session.query(User).count()
        total_images = db.session.query(Image).count()
        total_quizzes = db.session.query(Quiz).count()

        quiz_data = db.session.query(
            Quiz.name, db.func.count(Image.id).label('image_count')
        ).outerjoin(Image).group_by(Quiz.name).all()

        # Render the admin index page with the pie chart and additional data
        return self.render('admin/index.html', chart_data=chart_data, total_users=total_users, total_images=total_images, total_quizzes=total_quizzes, quiz_data=quiz_data)

# Custom ModelView with authentication and custom rendering
class MyModelView(ModelView):
    @requires_auth
    def is_accessible(self):
        return True

# Custom QuizView to include quiz ID
class QuizView(MyModelView):
    column_list = ('id', 'name', 'created')
    form_columns = ('id', 'name', 'created')

# Custom ImageView with image thumbnail, download icon, user name linked to user edit page, and quiz name
class ImageView(MyModelView):
    column_formatters = {
        'image_path': lambda v, c, m, p: Markup(
            f'<a href="#" onclick="showModal(\'{url_for("uploaded_file", quiz_id=m.quiz_id, filename=os.path.basename(m.image_path))}\')">'
            f'<img src="{url_for("uploaded_file", quiz_id=m.quiz_id, filename=os.path.basename(m.image_path))}" width="150"></a>'
        ),
        'download': lambda v, c, m, p: Markup(
            f'<a href="{url_for("uploaded_file", quiz_id=m.quiz_id, filename=os.path.basename(m.image_path))}" download>'
            f'<i class="fa fa-download"></i></a>'
        ),
        'user.name': lambda v, c, m, p: Markup(
            f'<a href="{url_for("user.edit_view", id=m.user.id)}">{m.user.name}</a>'
        ),
        'quiz.name': lambda v, c, m, p: m.quiz.name
    }
    column_list = ('image_path', 'quiz.name', 'user.name', 'phone_number', 'download')

    def __init__(self, session, **kwargs):
        super(ImageView, self).__init__(Image, session, **kwargs)

    def get_query(self):
        return self.session.query(self.model).options(joinedload(Image.user), joinedload(Image.quiz))

    def get_count_query(self):
        return self.session.query(db.func.count('*')).select_from(self.model)

# Admin setup
admin = Admin(
    app, 
    name='Admin', 
    template_mode='bootstrap3', 
    index_view=MyAdminIndexView(), 
    base_template='admin/custom_base.html'  # Specify your custom base template
)
admin.add_view(MyModelView(User, db.session, endpoint="user"))
admin.add_view(QuizView(Quiz, db.session))
admin.add_view(ImageView(db.session))

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
    # Debugging information
    logger.info(f"Serving file: {os.path.join(app.config['UPLOAD_FOLDER'], quiz_id, filename)}")
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], quiz_id), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
