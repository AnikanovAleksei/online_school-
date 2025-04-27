from django.core.management.base import BaseCommand
from users.models import Payment, SchoolUser
from school.models import Course, Lesson
from datetime import datetime


class Command(BaseCommand):
    help = 'Заполняет таблицу Payment тестовыми данными'

    def handle(self, *args, **options):

        user1 = SchoolUser.objects.get_or_create(email='user1@example.com')[0]
        user2 = SchoolUser.objects.get_or_create(email='user2@example.com')[0]

        course1 = Course.objects.get_or_create(title='Python Basics')[0]
        lesson1 = Lesson.objects.get_or_create(title='Урок 1', course=course1)[0]

        payments_data = [
            {
                'user': user1,
                'paid_course': course1,
                'paid_lesson': None,
                'amount': 5000,
                'payment_method': 'transfer',
            },
            {
                'user': user2,
                'paid_course': None,
                'paid_lesson': lesson1,
                'amount': 1000,
                'payment_method': 'cash',
            },
        ]

        for payment_data in payments_data:
            payment = Payment.objects.create(
                user=payment_data['user'],
                payment_date=datetime.now(),
                paid_course=payment_data['paid_course'],
                paid_lesson=payment_data['paid_lesson'],
                amount=payment_data['amount'],
                payment_method=payment_data['payment_method'],
            )
            self.stdout.write(self.style.SUCCESS(f'Создан платёж: {payment}'))

        self.stdout.write(self.style.SUCCESS('Успешно заполнено!'))
