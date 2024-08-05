# src/db/seeds.py

from src.models import db, User, Quiz, Image
from app import app

def seed_data():
    with app.app_context():
        # Drop existing data
        db.session.query(User).delete()
        db.session.query(Image).delete()
        db.session.query(Quiz).delete()
        db.session.commit()

        # Create initial users
        users = []
        for i in range(1, 41):
            user = User(
                name=f'User{i}',
                email=f'user{i}@example.com',
                phone=f'+12345678{i:02d}'
            )
            users.append(user)

        # Create initial quizzes
        quiz1 = Quiz(id='66377f58f77e650026c3c7c0', name='Скандинавский стиль', created='2024-06-17T08:25:37.928Z')
        quiz2 = Quiz(id='66a75a6e18108a0026d95d74', name='Стиль лофт', created='2024-06-18T08:25:37.928Z')
        quiz3 = Quiz(id='66a75aa95ac9fb00268cf1f8', name='Стиль минимализм', created='2024-06-19T08:25:37.928Z')
        quiz4 = Quiz(id='66a75abd17df430026dbf6a3', name='Стиль неоклассика', created='2024-06-20T08:25:37.928Z')
        quiz5 = Quiz(id='66a75ad49f61830026a976a9', name='Современный стиль', created='2024-06-21T08:25:37.928Z')

        # Add initial data to the session
        db.session.add_all(users + [quiz1, quiz2, quiz3, quiz4, quiz5])

        # Commit the session
        db.session.commit()
        
        user1 = users[0]
        user2 = users[1]

        # # Create initial images
        image1 = Image(quiz_id=quiz2.id, user_id=user1.id, image_path='generated_images/66a75a6e18108a0026d95d74/79111234567_1.png', phone_number=user1.phone)
        image2 = Image(quiz_id=quiz3.id, user_id=user2.id, image_path='generated_images/66a75aa95ac9fb00268cf1f8/79111234567_1.png', phone_number=user2.phone)
        image3 = Image(quiz_id=quiz3.id, user_id=user1.id, image_path='generated_images/66a75aa95ac9fb00268cf1f8/79111234567_2.png', phone_number=user1.phone)
        image4 = Image(quiz_id=quiz5.id, user_id=user2.id, image_path='generated_images/66a75ad49f61830026a976a9/79111234567_1.png', phone_number=user2.phone)
        image5 = Image(quiz_id=quiz2.id, user_id=user1.id, image_path='generated_images/66a75a6e18108a0026d95d74/79111234567_1.png', phone_number=user1.phone)
        image6 = Image(quiz_id=quiz3.id, user_id=user2.id, image_path='generated_images/66a75aa95ac9fb00268cf1f8/79111234567_1.png', phone_number=user2.phone)
        image7 = Image(quiz_id=quiz3.id, user_id=user1.id, image_path='generated_images/66a75aa95ac9fb00268cf1f8/79111234567_2.png', phone_number=user1.phone)
        image8 = Image(quiz_id=quiz5.id, user_id=user2.id, image_path='generated_images/66a75ad49f61830026a976a9/79111234567_1.png', phone_number=user2.phone)
        image9 = Image(quiz_id=quiz2.id, user_id=user1.id, image_path='generated_images/66a75a6e18108a0026d95d74/79111234567_1.png', phone_number=user1.phone)
        image10 = Image(quiz_id=quiz3.id, user_id=user2.id, image_path='generated_images/66a75aa95ac9fb00268cf1f8/79111234567_1.png', phone_number=user2.phone)
        image11 = Image(quiz_id=quiz3.id, user_id=user1.id, image_path='generated_images/66a75aa95ac9fb00268cf1f8/79111234567_2.png', phone_number=user1.phone)
        image12 = Image(quiz_id=quiz5.id, user_id=user2.id, image_path='generated_images/66a75ad49f61830026a976a9/79111234567_1.png', phone_number=user2.phone)

        # # Add images to the session
        db.session.add_all([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12])

        # # Commit the session
        db.session.commit()

        print("Database seeded successfully.")

# Usage example python -m src.db.seeds
if __name__ == '__main__':
    seed_data()
