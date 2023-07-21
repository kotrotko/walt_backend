from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from faker import Faker

from ..models import CustomUser


class TestUserRecordView(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.user = CustomUser.objects.create(email=self.fake.email())
        self.access_token = AccessToken.for_user(self.user)

    # def tearDown(self):
    #     # Clean up the database by deleting all CustomUser objects
    #     CustomUser.objects.all().delete()

    def test_user_create(self):
        fake = Faker()
        user = CustomUser.objects.create(email=fake.email())
        access_token = AccessToken.for_user(user)

        url = reverse('user_create')
        headers = {'Authorization': f'Bearer {str(self.access_token)}'}
        email = self.fake.email()
        password = "accountspassword"
        roles = 'jobseeker'

        response = self.client.post(url, {'email': email, 'password': password, 'roles': roles}, format='json', headers=headers)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_with_empty_email(self):

        url = reverse('user_create')
        headers = {'Authorization': f'Bearer {str(self.access_token)}'}
        email = '' # Empty email field
        password = "accountspassword"
        roles = 'jobseeker'

        response = self.client.post(url, {'email': email, 'password': password, 'roles': roles}, format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This field may not be blank.')
