from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from menu.models import Cuisine, Food, Type, BreakfastFood, DinnerFood, SupperFood
from .serializers import CuisineSerializer, FoodSerializer, TypeSerializer

@api_view(['GET',])
def cuisine_list(request):
    if request.method == "GET":
        cuisines = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisines, many=True)
        response = Response(serializer.data)
        return response
    
@api_view(['GET'])
def food_list(request):
    if request.method == 'GET':
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def types_list(request):
    if request.method == 'GET':
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def drinks_list(request):
    if request.method == 'GET':
        drinks = Food.objects.filter(type=Type.objects.get(name='Drink'))
        serializer = FoodSerializer(drinks, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def breakfast_list(request):
    if request.method == 'GET':
        food_ids = []
        for food in BreakfastFood.objects.all():
            food_ids.append(food.food.id)
        foods = Food.objects.filter(id__in=food_ids)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def dinner_list(request):
    if request.method == 'GET':
        food_ids = []
        for food in DinnerFood.objects.all():
            food_ids.append(food.food.id)
        foods = Food.objects.filter(id__in=food_ids)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def supper_list(request):
    if request.method == 'GET':
        food_ids = []
        for food in SupperFood.objects.all():
            food_ids.append(food.food.id)
        foods = Food.objects.filter(id__in=food_ids)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def review_list(request):
    if request.method == 'POST':
        pass
