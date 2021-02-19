from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model
from pages.models import UserReviews
from accounts.models import CustomUser
from .serializers import ReviewSerializer, ReviewSerializer2

@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = UserReviews.objects.all()        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class UserReview(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        if UserReviews.objects.filter(user=request.user).exists():
            review = UserReviews.objects.get(user=request.user)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(None)

    def post(self, request, *args, **kwargs):
        review, created = UserReviews.objects.get_or_create(user=request.user, content=request.data['content'], created_date=request.data['created_date'], rate=request.data['rate'])
        if created:
            serializer = ReviewSerializer(review)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        review = UserReviews.objects.get(user=request.user)
        review.content = request.data['content']
        review.created_date = request.data['created_date']
        review.rate = request.data['rate']
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

@api_view(['GET'])
def delete(request):
    review = UserReviews.objects.all().order_by('-created_data')[0]
    review.delete()
