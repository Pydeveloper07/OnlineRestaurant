from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('<int:id>/', views.get_foods, name='get_daily_offerings'),
]
