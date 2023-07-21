from django.urls import path
from .views import EmployerListCreateView, EmployerDetailView

urlpatterns = [
    path('employers/', EmployerListCreateView.as_view(), name='employer-list'),
    path('employers/<int:pk>', EmployerDetailView.as_view(), name='employer-detail')
]