from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import int_list_validator
import datetime
import math

class Bonus(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    threshold = models.IntegerField()

    def __str__(self):
        return self.name 
    
class UserBonus(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_bonus')
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE, related_name='users')
    created_date = models.DateField(editable=False, auto_now=True)

    def __str__(self):
        return self.user.username

class UserReviews(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='review')
    content = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now=True)
    rate = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Table(models.Model):
    capacity = models.IntegerField()
    duration = models.IntegerField(help_text='Duration to update price (in minutes)')
    price_per_duration = models.FloatField()

    def __str__(self):
        return str(self.id)

class ReservedTable(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reserved_times')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reserved_tables')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '{0}-{1}'.format(self.user.username, self.table.id)

    @staticmethod
    def get_total_price(start_time, end_time, duration, price_per_duration):
        st = datetime.timedelta(hours=int(start_time[0]), minutes=int(start_time[1]))
        et = datetime.timedelta(hours=int(end_time[0]), minutes=int(end_time[1]))
        difference_in_minutes = (et - st).total_seconds()/60
        return math.ceil(float(difference_in_minutes)/float(duration))*price_per_duration

class OrderHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='orders')  
    items_list = models.CharField(max_length=200, validators=[int_list_validator])
    items_quantity_list = models.CharField(max_length=200, validators=[int_list_validator])
    price = models.FloatField()
    delivery_fee = models.FloatField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def get_item_list(self):
        return list(self.items_list.split(','))
    
    def get_quantity_list(self):
        return list(self.items_quantity_list.split(','))

class ProcessingOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='processing_orders')
    items_list = models.CharField(max_length=200, validators=[int_list_validator])
    items_quantity_list = models.CharField(max_length=200, validators=[int_list_validator])
    address = models.CharField(max_length=500)
    contact_number = models.CharField(max_length=100)
    price = models.FloatField()
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def get_item_list(self):
        return list(self.items_list.split(','))

    def get_quantity_list(self):
        return list(self.items_quantity_list.split(','))

