from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import EmployerSerializer
from .models import Employer

class EmployerDetailView(RetrieveAPIView):
    serializer_class = EmployerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Employer.objects.all()
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployerListCreateView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Employer.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=serializer.validated_data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

