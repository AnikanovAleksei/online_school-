from rest_framework import serializers

from users.models import Subscription
from .models import Course, Lesson
from .validators import CourseLessonValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'link': {
                'required': False,
                'allow_null': True,
                'allow_blank': True
            }
        }
        validators = [
            CourseLessonValidator(field='link')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(source="lessons.all", many=True, read_only=True)

    is_subscribed = serializers.SerializerMethodField()

    validators = [CourseLessonValidator]

    class Meta:
        model = Course
        fields = ['name', 'description', 'lessons', 'lessons_count', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False
