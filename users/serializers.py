from rest_framework import serializers
from .models import Payment, SchoolUser


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SchoolUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = SchoolUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'avatar', 'password']
