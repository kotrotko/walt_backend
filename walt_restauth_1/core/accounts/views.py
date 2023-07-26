from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase, TokenRefreshView
from drf_spectacular.utils import extend_schema

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


# class UserRecordView(APIView):
class UserRecordView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # enables permission
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer

    @extend_schema(responses=CustomUserCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # user = serializer.save()
        try:
            user = serializer.save()
        except ValidationError as e:
            return Response({"email": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            # "id": user.id,
            "email": user.email,
            "roles": user.roles,
        }
        if user.pk is None:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
                response_data,
                status=status.HTTP_201_CREATED
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
