from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import Subscription
from .models import Course, SchoolUser


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = SchoolUser.objects.create(
            email='testuser@example.com',
            password='testpass123'
        )
        self.user.set_password('testpass123')
        self.user.save()

        # Создаем тестовый курс
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса'
        )

    def test_subscribe_success(self):
        """Тест успешной подписки на курс"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('school:subscription'),
            {'course_id': self.course.id},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_success(self):
        """Тест успешной отписки от курса"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('school:subscription'),
            {'course_id': self.course.id},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_unauthorized(self):
        """Тест попытки подписки без авторизации"""
        response = self.client.post(
            reverse('school:subscription'),
            {'course_id': self.course.id},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_invalid_course(self):
        """Тест подписки на несуществующий курс"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('school:subscription'),
            {'course_id': 999},  # Несуществующий ID
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_twice(self):
        """Тест двойной подписки и отписки"""
        self.client.force_authenticate(user=self.user)

        # Первый запрос - подписка
        response1 = self.client.post(
            reverse('school:subscription'),
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Второй запрос - отписка
        response2 = self.client.post(
            reverse('school:subscription'),
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Третий запрос - снова подписка
        response3 = self.client.post(
            reverse('school:subscription'),
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
