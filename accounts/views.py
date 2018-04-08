from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm


User = get_user_model()


def login_view(request):
    next_page = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        
        if next_page:
            return redirect(next_page)
        return redirect('/')

    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'form.html', context)


def register_view(request):
    next_page = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        
        if next_page:
            return redirect(next_page)
        return redirect('/')

    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'form.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
