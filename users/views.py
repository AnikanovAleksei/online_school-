from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Payment, SchoolUser
from .serializers import PaymentSerializer, SchoolUserSerializer
from .filters import PaymentFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


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
