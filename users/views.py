from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from school.models import Course
from .models import Payment, SchoolUser, Subscription
from .serializers import PaymentSerializer, SchoolUserSerializer
from .filters import PaymentFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']


class UserCreateAPIView(CreateAPIView):
    serializer_class = SchoolUserSerializer
    queryset = SchoolUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = SchoolUserSerializer
    queryset = SchoolUser.objects.all()

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = SchoolUserSerializer
    queryset = SchoolUser.objects.all()

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data['password'])
            user.save()


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = SchoolUserSerializer
    queryset = SchoolUser.objects.all()

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubscriptionAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
            status_code = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)
