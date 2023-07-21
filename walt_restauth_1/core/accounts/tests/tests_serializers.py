import time
import random

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import CustomUser
from ..serializers import CustomUserCreateSerializer


class TestCustomUserCreateSerializer(APITestCase):
    def setUp(self):
        # Initialize token as None
        self.token = None

    def tearDown(self):
        # Clean up the database by deleting all CustomUser objects
        CustomUser.objects.all().delete()

    def get_token(self):
        if self.token is None:
            refresh = RefreshToken()
            token = str(refresh.access_token)
        else:
            refresh = RefreshToken(self.token)
            token = str(refresh.access_token)

        return token

    @staticmethod
    def create_access_token(user):
        # Create a JWT access token for the user
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_user(self):
        # Set up test data
        url = reverse('user_create')
        timestamp = str(int(time.time()))
        random_suffix = str(random.randint(100, 999))
        email = f'test{timestamp}{random_suffix}@example.com'
        data = {
            'email': email,
            'password': 'testpassword',
            'roles': 'jobseeker'
        }

        # Create a user with different email for uniqueness
        user = CustomUser.objects.create(email='different@example.com', roles=data['roles'])

        user.set_password(data['password'])
        user.save()

        # Generate an access token for authentication
        access_token = self.create_access_token(user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # Send a POST request to create a user
        response = self.client.post(url, data)

        # Check if the response requires re-authentication
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            access_token = self.create_access_token(user)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer' + access_token)
            response = self.client.post(url, data)

        # Validate the serializer with provided data
        serializer = CustomUserCreateSerializer(data=data, context={'request': self.client.post(url, data)})
        is_valid = serializer.is_valid()

        # Debugging info
        # if not is_valid:
        #     print(serializer.errors)

        # Create the user if data is valid
        if is_valid:
            user = serializer.create(serializer.validated_data)
            # Perform assertions
            self.assertIsInstance(user, CustomUser)
            self.assertEqual(user.email, data['email'])
            self.assertTrue(user.check_password(data['password']))
            self.assertEqual(user.roles, data['roles'])

        # Ensure the response has a status code of 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_created_if_required_fields_missing(self):
        # Set up test data with missing 'password' field
        serializer_data = {
            'email': 'test@example.com',
            # 'password' field missing
            'role': 'admin',
        }

        # Create a serializer with missing field
        serializer = CustomUserCreateSerializer(data=serializer_data)

        # Ensure that calling is_valid() raises a ValidationError
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        # Check that the error messages contain the missing fields
        self.assertIn('password', serializer.errors)
