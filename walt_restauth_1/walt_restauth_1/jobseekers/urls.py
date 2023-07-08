from django.urls import path
from .views import JobseekerListCreateView, JobseekerDetailView

urlpatterns = [
    path('jobseekers/', JobseekerListCreateView.as_view(), name='jobseeker-list'),
    path('jobseekers/<int:pk>', JobseekerDetailView.as_view(), name='jobseeker-detail')
]