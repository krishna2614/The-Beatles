from django.urls import path
from .views import signin, register, _logout, forgot, profile
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('signin/', signin, name='accounts_signin'),
    path('register/', register, name='accounts_register'),
    path('logout/', _logout, name='accounts_logout'),
    path('forgot/', forgot, name='accounts_forgot'),
    path('profile/', profile, name='accounts_profile'),
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html', html_email_template_name='password_reset_email.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]
