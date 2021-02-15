from rest_framework import serializers
from pages.models import UserReviews
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['avatar']

class UserSerializer(serializers.ModelSerializer):
    avatar = CustomUserSerializer()
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'avatar']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserReviews
        fields = ['id', 'user', 'content', 'created_date', 'rate']
