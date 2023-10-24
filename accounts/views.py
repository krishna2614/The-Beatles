from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms
from .models import User


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        message = None
        form = forms.SigninForm()
        if request.method == 'POST':
            form = forms.SigninForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    message = f'Hello {user.username}! You have been logged in'
                    return redirect('index')
                else:
                    message = 'Login failed!'
        return render(request, 'signin.html', context={'form': form, 'message': message})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = forms.SignupForm()
        if request.method == 'POST':
            form = forms.SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                # auto-login user
                login(request, user)
                return redirect('accounts_signin')
        return render(request, 'register.html', context={'form': form})


def forgot(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = forms.ForgotPasswordForm()
        if request.method == 'POST':
            form = forms.ForgotPasswordForm(request.POST)
            if form.is_valid():
                u = User.objects.get(userId=request.user.userId)
                u.set_password('new password')
                u.save()
                # auto-login user
                login(request, u)
                return redirect('accounts_signin')
        return render(request, 'forgot_password.html', context={'form': form})


def _logout(request):
    logout(request)
    return redirect('accounts_signin')
