from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User
from django.shortcuts import render, redirect




def register(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return redirect(request, '404.html')
        new_user = User.objects.create(username=username, password=make_password(password))
        new_user.save()
        messages.success(request, 'registration successfull')
        return redirect('login')
    return render(request, 'register.html')


def login_user(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login success')
                return redirect('home')
            else:
                messages.error(request, 'Error')
                return render(request, 'login.html', {'message': "Please fill valid details"})
        return render(request, 'login.html')
    except Exception as e:
        print(e)
