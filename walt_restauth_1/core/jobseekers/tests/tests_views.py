from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from ..models import JobSeeker
from ...accounts.models import CustomUser


class JobseekerDetailViewTest(APITestCase):
    def setUp(self):
        dummy_cv_file = SimpleUploadedFile("cv.pdf", b"Dummy content", content_type="application/pdf")

        self.user = CustomUser.objects.create(email='user@foo.com')
        self.jobseeker = JobSeeker.objects.create(
            user=self.user,
            first_name='John Doe',
            phone_number='+95673407225',
            cv=dummy_cv_file,
        )
        self.access_token = AccessToken.for_user(self.user)

    def test_jobseeker_detail_view(self):
        url = reverse('jobseeker-detail', kwargs={'pk': self.jobseeker.pk})
        headers = {'Authorization': f'Bearer {str(self.access_token)}'}

        response = self.client.get(url, format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.jobseeker.first_name)
        self.assertEqual(response.data['phone_number'], self.jobseeker.phone_number)

        # Convert relative URL to absolute URL
        request = response.wsgi_request
        absolute_url = request.build_absolute_uri(self.jobseeker.cv.url)
        self.assertEqual(response.data['cv'], absolute_url)

class JobseekerListCreateViewTestCase(APITestCase):
    def setUp(self):

        # Create a few JobSeeker objects for testing the ListView
        self.user = JobSeeker.objects.create(first_name='John', phone_number='+123456789', cv='cv1.pdf')
        self.user = JobSeeker.objects.create(first_name='Jane', phone_number='+987654321', cv='cv2.pdf')
        self.user = JobSeeker.objects.create(first_name='Bob', phone_number='+555555555', cv='cv3.pdf')

    def test_list_jobseekers(self):
        url = reverse('jobseeker-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        jobseekers = JobSeeker.objects.all()

        # Convert relative URL to absolute URL
        request = response.wsgi_request

        for i, jobseeker in enumerate(jobseekers):
            self.assertEqual(response.data[i]['first_name'], jobseeker.first_name)
            self.assertEqual(response.data[i]['phone_number'], jobseeker.phone_number)
            absolute_url = request.build_absolute_uri(jobseeker.cv.url)
            self.assertEqual(response.data[i]['cv'], absolute_url)

            user = jobseeker.user

            filtered_jobseeker = JobSeeker.objects.filter(user=user, first_name='John').first()

            self.assertIsNotNone(filtered_jobseeker)
