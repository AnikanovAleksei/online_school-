from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Lesson, Course
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users.models import SchoolUser


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email="admin@test.ru")
        moder_group, created = Group.objects.get_or_create(name='moders')
        self.user.groups.add(moder_group)
        self.course = Course.objects.create(name="Профессор математики",
                                            description="Стань лучшим с этим курсом", owner=self.user)
        self.lesson = Lesson.objects.create(name="Математика", course=self.course, description="Лучшие уроки")
        self.client.force_authenticate(user=self.user)

    # def test_course_retrieve(self):
    #     url = reverse("school:courses-detail", args=(self.course.pk,))
    #     response = self.client.get(url)
    #
    #     # Проверка статус-кода
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     # Проверка содержимого ответа (добавлено использование data)
    #     data = response.json()
    #     self.assertEqual(data['id'], self.course.pk)  # Пример проверки ID
    #     self.assertIn('name', data)  # Проверка наличия поля


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.moder_group = Group.objects.create(name='moders')

        self.regular_user = SchoolUser.objects.create(
            email='user@test.com',
            password='testpass123',
            first_name='Regular',
            last_name='User'
        )
        self.regular_user.set_password('testpass123')
        self.regular_user.save()

        self.moderator_user = SchoolUser.objects.create(
            email='moderator@test.com',
            password='testpass123',
            first_name='Moderator',
            last_name='User'
        )
        self.moderator_user.set_password('testpass123')
        self.moderator_user.save()
        self.moderator_user.groups.add(self.moder_group)

        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса',
            owner=self.regular_user
        )

        self.lesson = Lesson.objects.create(
            name='Тестовый урок',
            description='Описание урока',
            course=self.course,
            owner=self.regular_user
        )

        self.create_url = reverse('school:lesson_create')
        self.list_url = reverse('school:lesson_list')
        self.detail_url = reverse('school:lesson_retrieve', args=[self.lesson.id])
        self.update_url = reverse('school:lesson_update', args=[self.lesson.id])
        self.delete_url = reverse('school:lesson_destroy', args=[self.lesson.id])

    def test_lesson_list_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(reverse('school:lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_list_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('school:lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_retrieve_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(reverse('school:lesson_retrieve', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Тестовый урок')

    def test_lesson_retrieve_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('school:lesson_retrieve', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_as_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)
        data = {'name': 'Обновленный урок'}
        response = self.client.patch(reverse('school:lesson_update', args=[self.lesson.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Обновленный урок')

    def test_lesson_update_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Обновленный урок'}
        response = self.client.patch(reverse('school:lesson_update', args=[self.lesson.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_as_regular_user(self):
        self.regular_user.groups.clear()

        lesson_to_delete = Lesson.objects.create(
            name='Урок для удаления',
            description='Описание',
            course=self.course,
            owner=self.regular_user,
            link='https://youtube.com/delete_me'
        )

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(
            reverse('school:lesson_destroy', args=[lesson_to_delete.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=lesson_to_delete.pk).exists())

    def test_lesson_delete_as_moderator_forbidden(self):
        """Проверка, что модератор не может удалять"""
        lesson = Lesson.objects.create(
            name='Урок',
            description='Описание',
            course=self.course,
            owner=self.regular_user,
            link='https://youtube.com/test'
        )

        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.delete(
            reverse('school:lesson_destroy', args=[lesson.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
