from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, UserSerializerWithToken
from accounts.models import CustomUser


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
        print(request.data)
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
