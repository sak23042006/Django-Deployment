from rest_framework import serializers
from .models import User, Grounds
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return User.objects.create(**validated_data)

class GroundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grounds
        fields = ['groundname', 'gamename', 'location', 'price', 'slots', 'image']