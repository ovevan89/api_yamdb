from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from review.models import User


def send_user_email(username, email):
    """Отправка письма с токеном пользователю."""
    user = get_object_or_404(User, username=username)
    send_mail(
        'Регистрация в сервисе Yamdb',
        f'Your code is here {default_token_generator.make_token(user)}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
