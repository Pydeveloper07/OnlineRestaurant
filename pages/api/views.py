from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from django.core.mail import BadHeaderError, send_mail
import smtplib
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

@api_view(['POST'])
def contact(request):
    if request.method == 'POST':
        subject = request.data['subject']
        email = request.data['email']
        message = request.data['message']
        if email and message:
            try:
                send_mail(
                    subject, 
                    'From: {0}\n{1}'.format(email, message), 
                    email, 
                    ['fantasyrestaurantt@gmail.com'],
                    fail_silently=False
                    )
                return Response({'message': 'Success!'}, status=status.HTTP_200_OK)
            except BadHeaderError:
                return Response({'message': 'Invalid Header found!'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message': 'Something went wrong in the server:( Try again!'}, status=status.HTTP_400_BAD_REQUEST)
        