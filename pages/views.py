from django.shortcuts import render, get_object_or_404, redirect
from .models import ReservedTable, UserReviews
from django.contrib import messages
from menu.models import Food
import datetime

def index(request):
    discount_foods = Food.objects.exclude(discount=None).exclude(discount=0)
    reviews = UserReviews.objects.all().order_by('-created_date')
    sum = 0
    for review in reviews:
        sum += review.rate
    average_rating = round(sum/reviews.count(), 1)
    context = {
        'foods': discount_foods,
        'reviews': reviews,
        'average_rating': average_rating
    }
    return render(request, 'pages/index.html', context)

def rate(request):
    if request.method == "POST":
        status = request.POST['review_status']
        user = request.user
        content = request.POST['content']
        rate = request.POST['rating']
        if status == 'new':
            new_review = UserReviews.objects.create(user_id=user, content=content, rate=rate)
            new_review.save()
            messages.success(request, 'Your review has been recorded!')
            return redirect('index')
        if status == 'updating':
            review = UserReviews.objects.get(user_id=user.id)
            review.content = content
            review.rate = rate
            review.save(update_fields=['content', 'rate'])
            messages.success(request, 'Review edition succeeded!')
            return redirect('index')

            

