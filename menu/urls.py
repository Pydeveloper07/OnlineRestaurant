from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('<int:id>/', views.get_foods, name='get_daily_offerings'),
    path('drinks/', views.get_drinks, name='drinks'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
]
