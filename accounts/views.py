from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pages.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages

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
        conf_password = request.POST['conf_password']
        if password != conf_password:
            messages.error(request, 'Password do not match!')
            return redirect('index')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username already taken! Try another!')
            return redirect('index')
        user = User.objects.create_user(
            username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        custom_user = CustomUser.objects.create(
            user_id=user,
            avatar=request.FILES['avatar'],
            phone_number=phone_number,
            address=address
        )
        custom_user.save()
        messages.success(request, 'Registration succeeded! Enjoy our services!')
        return redirect('index')
            

