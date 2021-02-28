from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list),
    path('user-review/', views.UserReview.as_view()),
    path('contact/', views.contact),
    path('tables/', views.table_list),
    path('tables/<int:pk>/', views.check_table),
    path('user-tables/', views.get_user_tables),
    path('order-table/', views.order_table),
    path('order/', views.order),
    path('user-order-history/', views.get_user_orders)
]