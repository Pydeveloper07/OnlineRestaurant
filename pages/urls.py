from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rate/', views.rate, name='rate'),
    path('get_tables/', views.get_tables, name='get_tables'),
    path('check_table/', views.check_table, name='check_table'),
    path('check_table_capacity/', views.check_capacity, name='check_table_capacity'),
    path('check_res_time/', views.check_res_time, name='check_res_time'),
    path('order_table/', views.order_table, name='order_table'),
]