from rest_framework import serializers
from pages.models import UserReviews, Table, ReservedTable, OrderHistory
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

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'capacity', 'duration', 'price_per_duration']

class ReservedTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedTable
        fields = ['id', 'start_time', 'end_time']
