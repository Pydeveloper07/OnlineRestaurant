from django.shortcuts import render, get_object_or_404
from .models import ReservedTable, UserReviews
from menu.models import Food
import datetime

def index(request):
    discount_foods = Food.objects.exclude(discount=None).exclude(discount=0)
    reviews = UserReviews.objects.all().order_by('-created_date')
    context = {
        'foods': discount_foods,
        'reviews': reviews
    }
    return render(request, 'pages/index.html', context)
