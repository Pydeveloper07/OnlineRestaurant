from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BreakfastFood, DinnerFood, SupperFood, Cuisine, Type, Food
from .models import FoodLikes, FoodDislikes
from django.http import Http404, HttpResponse
import json


def menu(request):
    cuisines = Cuisine.objects.all()
    types = Type.objects.exclude(name='Drink')
    context = {
        'cuisines': cuisines,
        'types': types,
    }
    return render(request, 'menu/foods.html', context)

def get_foods(request, id):
    if id == 1:
        title = 'Breakfast'
        foods = BreakfastFood.objects.all()
    elif id == 2:
        title = 'Dinner'
        foods = DinnerFood.objects.all()
    elif id == 3:
        title = 'Supper'
        foods = SupperFood.objects.all()
    else:
        raise Http404("Undefined choice!")
    context = {
        'title': title,
        'foods': foods,
    }
    return render(request, 'menu/listings.html', context) 

def get_drinks(request):
    type_food = get_object_or_404(Type, name='Drink')
    drinks = None
    if type_food:
        drinks = type_food.foods.all()
    title = 'Drinks'

    context = {
        'title': title,
        'foods': drinks,
    }
    return render(request, 'menu/listings.html', context)

@login_required
def like(request):
    if request.method == 'POST':
        id = request.POST['foodId']
        user = request.user.id
        existed = False
        status = ''
        number_of_likes = 0
        number_of_dislikes = 0
        if FoodLikes.objects.filter(user=user, food=id).exists():
            status = 'unlike'
            FoodLikes.objects.filter(user=user, food=id).delete()
            number_of_likes = FoodLikes.objects.filter(food=id).count()
            context = {
                'existed': existed,
                'status': status,
                'numOfLikes': number_of_likes
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')
        else:
            if FoodDislikes.objects.filter(user=user, food=id).exists():
                FoodDislikes.objects.get(user=user, food=id).delete()
                existed = True
                number_of_dislikes = FoodDislikes.objects.filter(food=id).count()
            status = 'like'
            new = FoodLikes.objects.create(user=request.user, food=Food.objects.get(id=id))
            new.save()
            number_of_likes = FoodLikes.objects.filter(food=id).count()
            context = {
                'existed': existed,
                'status': status,
                'numOfLikes': number_of_likes,
                'numOfDislikes': number_of_dislikes
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')

@login_required
def dislike(request):
    if request.method == 'POST':
        id = request.POST['foodId']
        user = request.user.id
        existed = False
        status = ''
        number_of_likes = 0
        number_of_dislikes = 0
        if FoodDislikes.objects.filter(user=user, food=id).exists():
            status = 'undislike'
            FoodDislikes.objects.filter(user=user, food=id).delete()
            number_of_dislikes = FoodDislikes.objects.filter(food=id).count()
            context = {
                'existed': existed,
                'status': status,
                'numOfDislikes': number_of_dislikes
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')
        else:
            if FoodLikes.objects.filter(user=user, food=id).exists():
                FoodLikes.objects.get(user=user, food=id).delete()
                existed = True
                number_of_likes = FoodLikes.objects.filter(food=id).count()
            status = 'dislike'
            new = FoodDislikes.objects.create(
                user=request.user, food=Food.objects.get(id=id))
            new.save()
            number_of_dislikes = FoodDislikes.objects.filter(food=id).count()
            context = {
                'existed': existed,
                'status': status,
                'numOfLikes': number_of_likes,
                'numOfDislikes': number_of_dislikes
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')

def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        id = request.POST['food_id']
        quantity = request.POST['quantity']
        if not 'foods' in request.session.keys():
            request.session['foods'] = {}
        if id in request.session['foods'].keys():
            request.session['foods'][id] = int(request.session['foods'][id]) + int(quantity)
        else:
            request.session['foods'][id] = quantity
        context = {
            'message': 'Success'
        }
        print(request.session['foods'])
        return HttpResponse(json.dumps(context), content_type='applications/json')
    else:
        context = {
            'login_required': True
        }
        return HttpResponse(json.dumps(context), content_type='applications/json')

