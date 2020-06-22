from django.contrib import admin
from .models import Cuisine, Type, Food, BreakfastFood, DinnerFood, SupperFood

admin.site.register(Cuisine)
admin.site.register(Type)
admin.site.register(Food)
admin.site.register(BreakfastFood)
admin.site.register(DinnerFood)
admin.site.register(SupperFood)
