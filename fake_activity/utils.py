import random
from faker import Faker
from users.models import CustomUser
from news.models import Post

fake = Faker()

def create_fake_users_and_posts(user_count=10, post_count=5):
    created_users = []
    for _ in range(user_count):
        username = fake.user_name()
        email = fake.email()
        password = "password123"
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Создаем пользователя
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        created_users.append(user)

        # Генерация постов для пользователя
        for _ in range(post_count):
            content = fake.text(max_nb_chars=200)
            Post.objects.create(
                author=user,
                content=content
            )
    return created_users
