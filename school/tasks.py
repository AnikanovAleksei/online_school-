from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from users.models import Subscription


@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная задача для отправки уведомлений об обновлении курса
    (версия с текстом прямо в коде, без HTML-шаблона)
    """
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user', 'course')

    for subscription in subscriptions:
        user = subscription.user
        course = subscription.course

        subject = f'Обновление курса "{course.name}"'

        message = f"""Здравствуйте, {user.first_name}!

Курс "{course.name}", на который вы подписаны, был обновлён.

Описание курса: {course.description}

С уважением,
Команда вашей образовательной платформы
"""

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
