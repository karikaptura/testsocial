from django.core.management.base import BaseCommand
from users.models import CustomUser
from profiles.models import Profile
from news.models import Post
from django.core.files.base import ContentFile
import requests
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Generate fake users and activity"

    def handle(self, *args, **kwargs):
        fake_users_count = 10  # Количество фейковых пользователей
        max_posts_per_user = 5  # Максимальное количество постов на пользователя
        profile_photo_url = "https://thispersondoesnotexist.com/image"  # URL для генерации портретов
        post_image_api = "https://picsum.photos/800/600"  # API для генерации изображений для постов

        for _ in range(fake_users_count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}"
            email = f"{username}@example.com"
            password = "password123"

            # Создаем пользователя
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Настраиваем профиль пользователя
            profile = Profile.objects.get(user=user)
            profile.bio = fake.sentence()

            # Загружаем портрет
            response = requests.get(profile_photo_url, timeout=10)
            if response.status_code == 200:
                profile.avatar.save(
                    f"{username}_avatar.jpg",
                    ContentFile(response.content)
                )

            profile.save()

            # Создаем посты
            post_count = random.randint(1, max_posts_per_user)
            for _ in range(post_count):
                post_content = fake.text(max_nb_chars=200)
                post_image_response = requests.get(post_image_api)

                post = Post.objects.create(
                    author=user,
                    content=post_content
                )

                # Добавляем изображение к посту
                if post_image_response.status_code == 200:
                    post.image.save(
                        f"{username}_post_image.jpg",
                        ContentFile(post_image_response.content)
                    )

                post.save()

            self.stdout.write(f"Создан пользователь: {first_name} {last_name} (username: {username}) с {post_count} постами.")


'''
class Command(BaseCommand):
    help = "Создает фейковых пользователей и посты"

    def handle(self, *args, **kwargs):
        created_users = create_fake_users_and_posts()
        ActivityLog.objects.create(
            activity_type="Создание пользователей и постов через команду",
            details=f"Создано {len(created_users)} пользователей с постами."
        )
        self.stdout.write(f"Создано {len(created_users)} пользователей с постами.")
'''