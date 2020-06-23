from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import int_list_validator
import os
import datetime
import math

def user_image_upload_path(instance, filename):
    filename = instance.user_id.username + '.jpg'
    return os.path.join('users', filename)

class CustomUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    avatar = models.ImageField(max_length=200, upload_to=user_image_upload_path, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user_id.username

class Bonus(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()

    def __str__(self):
        return self.name
    
class UserBonus(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_bonus')
    bonus_id = models.ForeignKey(Bonus, on_delete=models.CASCADE, related_name='users')
    created_date = models.DateField(editable=False, auto_now=True)

    def __str__(self):
        return self.user_id.username

class UserReviews(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    content = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now=True)
    rate = models.IntegerField()

    def __str__(self):
        return self.user_id.username
    
class Table(models.Model):
    capacity = models.IntegerField()
    duration = models.IntegerField(help_text='Duration to update price (in minutes)')
    price_per_duration = models.FloatField()

    def __str__(self):
        return str(self.id)

class ReservedTable(models.Model):
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reserved_times')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserved_tables')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '{0}-{1}'.format(self.user_id.username, self.table_id.id)

    def get_total_price(self):
        start_time = datetime.timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
        end_time = datetime.timedelta(hours=self.end_time.hour, minutes=self.end_time.minute)
        difference_in_minutes = (end_time - start_time).total_seconds()/60
        return math.ceil(float(difference_in_minutes)/float(self.table_id.duration))*self.table_id.price_per_duration

class OrderHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')  
    items_list = models.CharField(max_length=200, validators=[int_list_validator])
    items_quantity_list = models.CharField(max_length=200, validators=[int_list_validator])
    price = models.FloatField()
    delivery_fee = models.FloatField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id.username
    
    def get_item_list(self):
        return list(items_list.split(','))
    
    def get_quantity_list(self):
        return list(items_quantity_list.split(','))

class ProcessingOrder(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processing_orders')
    items_list = models.CharField(max_length=200, validators=[int_list_validator])
    items_quantity_list = models.CharField(max_length=200, validators=[int_list_validator])
    address = models.CharField(max_length=500)
    contact_number = models.CharField(max_length=100)
    price = models.FloatField()
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id.username
    
    def get_item_list(self):
        return list(items_list.split(','))

    def get_quantity_list(self):
        return list(items_quantity_list.split(','))
 
