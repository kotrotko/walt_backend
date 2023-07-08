from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase, TokenRefreshView

from .serializers import CustomUserCreateSerializer, TokenObtainPairSerializer, PasswordResetSerializer
from .models import CustomUser


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class TokenRefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class UserRecordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # enables permission
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_queryset(self):
        return self.queryset

    def email_confirm_redirect(request, key):
        return HttpResponseRedirect(
            f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
        )

    def password_reset_confirm_redirect(request, uidb64, token):
        return HttpResponseRedirect(
            f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
        )
