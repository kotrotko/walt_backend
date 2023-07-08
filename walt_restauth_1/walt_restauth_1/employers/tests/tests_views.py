from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from ..models import Employer
from ...accounts.models import CustomUser


class EmployerDetailViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@foo.com')
        self.employer = Employer.objects.create(
            user=self.user,
            company_name='Test Company',
            company_description='This is a test company description',
            website='https://www.example.com',
        )
        self.access_token = AccessToken.for_user(self.user)

    def test_employer_detail_view(self):
        url = reverse('employer-detail', kwargs={'pk': self.employer.pk})
        headers = {'Authorization': f'Bearer {str(self.access_token)}'}

        response = self.client.get(url, format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], self.employer.company_name)
        self.assertEqual(response.data['company_description'], self.employer.company_description)
        self.assertEqual(response.data['website'], self.employer.website)
