from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import SchoolUser


@shared_task
def block_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = SchoolUser.objects.filter(
        last_login__lt=month_ago,
        is_active=True
    )
    count = inactive_users.update(is_active=False)
    return f"Заблокировано {count} пользователей"
