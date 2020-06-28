from django.shortcuts import render, get_object_or_404
from .models import BreakfastFood, DinnerFood, SupperFood, Cuisine, Type
from django.http import Http404


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
