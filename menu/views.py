from django.shortcuts import render
from .models import BreakfastFood, DinnerFood, SupperFood
from django.http import Http404


def menu(request):
    return render(request, 'menu/foods.html')

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
