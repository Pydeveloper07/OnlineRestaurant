from django.db import models
from django.contrib.auth.models import User
import os

def cuisine_image_upload_path(instance, filename):
    filename = instance.name + '.jpg'
    return os.path.join('menu', 'cuisines', filename)

def type_image_upload_path(instance, filename):
    filename = instance.name + '.jpg'
    return os.path.join('menu', 'types', filename)

def food_image_upload_path(instance, filename):
    filename = instance.name + '.jpg'
    return os.path.join('menu', instance.type_id.name, filename)

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(max_length=500, upload_to=cuisine_image_upload_path)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(max_length=500, upload_to=type_image_upload_path)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.FloatField()
    total_orders = models.IntegerField(editable=False, null=True)
    image = models.ImageField(max_length=500, upload_to=food_image_upload_path)
    discount = models.FloatField(null=True, blank=True, help_text='Enter value in %')
    cuisine_id = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True, related_name='foods')
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='foods')

    def get_current_price(self):
        if self.discount:
            return self.price*(1 - self.discount/100)
        else:
            return self.price

    def __str__(self):
        return self.name
    
class FoodLikes(models.Model):
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='likes')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='likes')

class FoodDislikes(models.Model):
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='dislikes')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dislikes')

class BreakfastFood(models.Model):
    food_id = models.OneToOneField(Food, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_id.name

class DinnerFood(models.Model):
    food_id = models.OneToOneField(Food, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_id.name

class SupperFood(models.Model):
    food_id = models.OneToOneField(Food, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_id.name
