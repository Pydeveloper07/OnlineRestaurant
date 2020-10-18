from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/<str:username>', views.dashboard, name='dashboard'),
    path('editProfile/', views.edit_profile, name='edit_profile'),
    path('checkUsername/', views.check_username, name='check_username'),
]