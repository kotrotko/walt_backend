from django.contrib import admin
from django.urls import include, path
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('core.accounts.urls')),

    # Token-related URLs
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'), # This endpoint is to obtain a token pair (refresh token and access token) by providing valid credentials (username/email and password) in the request payload.
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'), # This endpoint is to refresh an expired access token by providing a valid refresh token in the request payload.
    path('api/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'), # This endpoint is to verify the authenticity of an access token by providing a valid access token in the request payload.

    # allauth URLs
    path('accounts/', include('allauth.urls')), # These URLs are provided by the Allauth library and handle various authentication-related functionality, such as login, registration, password reset, etc.

    # Auth URLs (custom authentication URLs)
    path('api/auth/', include('core.accounts.urls')), # This prefix is used for custom authentication URLs defined in the accounts.urls module.

    # Employers and Jobseekers URLs
    path('employers/', include('core.employers.urls')),
    path('jobseekers/', include('core.jobseekers.urls')),

    # Password Reset URLs
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uid64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]