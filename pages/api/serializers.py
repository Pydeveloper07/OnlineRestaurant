from rest_framework import serializers
from pages.models import UserReviews
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'avatar']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserReviews
        fields = ['id', 'user', 'content', 'created_date', 'rate']

class ReviewSerializer2(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserReviews
        fields = ['user', 'created_date', 'content', 'rate']
