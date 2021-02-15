from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pages.models import UserReviews
from .serializers import ReviewSerializer
import json

@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        review_array = []
        reviews = UserReviews.objects.all()
        for review in reviews:
            r_dic = {}
            r_dic['user'] = {
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'username': review.user.username
            }
            r_dic['content'] = review.content
            r_dic['created_date'] = review.created_date.isoformat()
            r_dic['rate'] = review.rate
            review_array.append(r_dic)
        
        serializer = ReviewSerializer(review_array, many=True)
        return Response(serializer.data)