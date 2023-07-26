from django.urls import path

from dj_rest_auth.registration.views import (RegisterView, ResendEmailVerificationView, VerifyEmailView)
from dj_rest_auth.views import (LoginView, LogoutView, UserDetailsView, PasswordResetConfirmView, PasswordResetView)

from .views import UserRecordView

urlpatterns = [
    # User-related URLs
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),

    # Registration and email verification UPLs
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('register/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('register/resend-email/', ResendEmailVerificationView.as_view(), name='rest_resend_email'),

    # Login and logout URLs
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),

    # Password reset URLs
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Email confirmation views
    path('account-confirm-email/<str:key>/', UserRecordView.email_confirm_redirect, name='account_confirm_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('password/reset/confirm/<str:uidb64>,/<str:token>/', UserRecordView.password_reset_confirm_redirect, name='password_reset_confirm'),
]