from rest_framework import serializers
from pages.models import UserReviews
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserReviews
        fields = ['user', 'content', 'created_date', 'rate']