from rest_framework import serializers
from .models import User, Grounds
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','firstname', 'lastname', 'email', 'phone', 'password', 'confirm_password']

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
        # Remove confirm_password as it should not be passed to the User model
        validated_data.pop('confirm_password', None)

        # Create the user instance with the remaining validated data
        # password = validated_data.pop('password')
        user = User(**validated_data)  # Pass only fields present in the User model
        # user.set_password(password)  # Hash the password before saving
        user.save()
        return user



class GroundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grounds
        fields = ['groundname', 'gamename', 'location', 'price', 'slots', 'image']