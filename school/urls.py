from rest_framework.routers import DefaultRouter

from users.views import SubscriptionAPIView
from .views import (CourseViewSet, LessonCreateApiView, LessonListApiView, LessonUpdateApiView, LessonDestroyApiView,
                    LessonRetrieveApiView)
from school.apps import SchoolConfig
from django.urls import path


app_name = SchoolConfig.name
router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/', LessonListApiView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_retrieve'),
    path('lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson_destroy'),
    path('lesson/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
] + router.urls
