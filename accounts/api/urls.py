from django.urls import path
from .views import current_user, UserList, update_user
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('user-update/', update_user),
]