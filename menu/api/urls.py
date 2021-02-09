from django.urls import path
from . import views

urlpatterns = [
    path('cuisines/', views.cuisine_list),
    path('types/', views.types_list),
    path('foods/', views.food_list),
    path('drinks/', views.drinks_list),
    path('breakfast/', views.breakfast_list),
    path('dinner/', views.dinner_list),
    path('supper/', views.supper_list)
]