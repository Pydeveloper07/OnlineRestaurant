from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list),
    path('user-review/', views.UserReview.as_view()),
    path('delete/', views.delete)
]