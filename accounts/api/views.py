from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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
