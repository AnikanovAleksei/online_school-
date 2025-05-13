from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsNotModer
from .models import Course, Lesson
from .paginators import CourseLessonPaginator
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .tasks import send_course_update_notification


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        send_course_update_notification.delay(instance.id)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModer]
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer]
    pagination_class = CourseLessonPaginator


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer]

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы можете удалять только свои уроки")
        instance.delete()
