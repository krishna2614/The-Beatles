from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from .forms import ProfileForm
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
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        form = forms.ForgotPasswordForm()
        if request.method == 'POST':
            form = forms.ForgotPasswordForm(request.POST)
            if form.is_valid():
                user = authenticate(request, userId=request.user.userId, password=form.cleaned_data['old_password'])
                if user:
                    u = User.objects.get(userId=request.user.userId)
                    u.set_password(form.cleaned_data['new_password'])
                    u.save()
                    # auto-login user
                    login(request, u)
                    return redirect('index')
                else:
                    print('PASSWORD INCORRECT')
                    return render(request, 'forgot_password.html', context={'form': form})
            print('FORM NOT VALID')
            return render(request, 'forgot_password.html', context={'form': form})
        return render(request, 'forgot_password.html', context={'form': form})


def _logout(request):
    logout(request)
    return redirect('accounts_signin')


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            print('Form Valid')
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('index')  # Redirect to the profile page
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

