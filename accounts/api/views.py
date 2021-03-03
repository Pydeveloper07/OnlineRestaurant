from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, UserSerializerWithToken
from accounts.models import CustomUser
from pages.models import Bonus, UserBonus


@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def current_user(request):
    if CustomUser.objects.filter(username=request.user.username).exists():
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response(None)


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_bonus = UserBonus.objects.create(
                user=get_user_model().objects.get(username=request.data['username']),
                bonus=Bonus.objects.get(name='Simple')
                )
            user_bonus.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated,])
def update_user(request):
    print(request.data)
    if request.method == 'PUT':
        user = request.user
        if request.data['username']:
            user.username = request.data['username']
        if request.data['first_name']:
            user.first_name = request.data['first_name']
        if request.data['last_name']:
            user.last_name = request.data['last_name']
        if request.data['email']:
            user.email = request.data['email']
        if request.data['phone_number']:
            user.phone_number = request.data['phone_number']
        if request.data['address']:
            user.address = request.data['address']
        if request.data['avatar']:
            user.avatar = request.data['avatar']
        try:
            user.save()
        except:
            return Response(status=status.HTTP_401_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    return Response(status=status.HTTP_401_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_user_status(request):
    if request.method == 'GET':
        user_status = {}
        user_status['status'] = request.user.user_bonus.bonus.name
        user_status['status_bonus'] = request.user.user_bonus.bonus.value
        user_status['total_orders'] = request.user.orders.all().count()
        total_expense = 0
        for order in request.user.orders.all():
            total_expense += order.price
        user_status['total_expenses'] = total_expense
        return Response(user_status)
    return Response(status=status.HTTP_401_BAD_REQUEST)
