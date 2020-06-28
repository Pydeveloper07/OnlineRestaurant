from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('<int:id>/', views.get_foods, name='get_daily_offerings'),
    path('drinks/', views.get_drinks, name='drinks'),
]
