from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pages.models import CustomUser
from menu.models import Food
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
import json

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong credentials!')
            return redirect('index')
        else:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('index')

@login_required
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You have successfully logged out!")
        return redirect('index')

def register(request):
    if request.method == 'POST':
        first_name = last_name = ''
        username = request.POST['username']
        if request.POST['first_name']:
            first_name = request.POST['first_name']
        if request.POST['last_name']:
            last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = User.objects.create_user(
            username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        custom_user = CustomUser.objects.create(
            user_id=user,
            avatar=request.FILES.get('avatar', None),
            phone_number=phone_number,
            address=address
        )
        custom_user.save()
        messages.success(request, 'Registration succeeded! Enjoy our services!')
        return redirect('index')
            
def edit_profile(request):
    if request.method == "POST":
        user = get_object_or_404(User, id=request.user.id)
        username = first_name = last_name = email = address = phone_number = None
        avatar = user.custom_user.avatar
        if not user:
            return Http404()
        if request.POST['username']:
            username = request.POST['username']
        if request.POST['first_name']:
            first_name = request.POST['first_name']
        if request.POST['last_name']:
            last_name = request.POST['last_name']
        if request.POST['email']:
            email = request.POST['email']
        if request.POST['address']:
            address = request.POST['address']
        if request.POST['phone_number']:
            phone_number = request.POST['phone_number']
        if 'avatar' in request.FILES:
            if request.FILES['avatar']:
                avatar = request.FILES['avatar']
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        custom_user = get_object_or_404(CustomUser, user_id=user.id)
        if not custom_user:
            return Http404()
        custom_user.address = address
        custom_user.phone_number = phone_number
        custom_user.avatar = avatar
        user.save(update_fields=['username', 'first_name', 'last_name', 'email'])
        custom_user.save(update_fields=['address', 'phone_number', 'avatar'])
        messages.success(request, 'Your profile successfully updated!')
        return redirect('dashboard', user.username)


def check_username(request):
    if request.method == 'POST':
        username = request.POST['username']
        error = True
        message = ''
        if username == request.user.username:
            error = False
            message = 'Username not changing!'
        else:
            if User.objects.filter(username=username).exists():
                error = True
                message = 'Username is not available'
            else:
                error = False
                message = 'Username is available!'
        context = {
            'error': error,
            'message': message
        }
        return HttpResponse(json.dumps(context), content_type='applications/json')


def dashboard(request, username):
    orders = request.user.orders.all()
    num_of_orders = orders.count()
    total_expense = 0
    for order in orders:
        total_expense += order.price + order.delivery_fee
    order_list = {}
    i = 0
    for order in orders:
        food_list = {}
        item_list = order.get_item_list()
        quantity_list = order.get_quantity_list()
        for j in range(len(item_list)):
            if Food.objects.filter(pk=item_list[j]).exists():
                food = Food.objects.get(pk=item_list[j])
                quantity = quantity_list[j]
                food_list['{0}'.format(j+1)] = {
                    'food': food,
                    'quantity': quantity
                }
        # order_list['{0}'.format(i+1)] = food_list
        order_list['{0}'.format(i+1)] = {}
        order_list['{0}'.format(i+1)]['foods'] = food_list
        order_list['{0}'.format(i+1)]['total_cost'] = order.price + order.delivery_fee
        order_list['{0}'.format(i+1)]['created_date'] = order.created_date
        i += 1
    print(order_list)
    context = {
        'number_of_orders': num_of_orders,
        'total_expense': total_expense,
        'orders': order_list
    }
    return render(request, 'accounts/dashboard.html', context)
