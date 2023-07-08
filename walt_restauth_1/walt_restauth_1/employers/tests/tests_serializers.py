from django.test import TestCase

from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from ..models import Employer
from ..serializers import EmployerSerializer
from ...accounts.models import CustomUser


class EmployerSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword', roles='employer')
        self.employer_token = AccessToken.for_user(self.user)

    def test_case_employer_authorized(self):
        data = {
            'company_name': 'Test Company',
            'company_description': 'Test Description',
            'website': 'https://www.example.com',
        }
        request = self.factory.post('/employers/', data, HTTP_AUTHORIZATION=f'Bearer {self.employer_token}')
        request.user = self.user
        serializer = EmployerSerializer(data=data, context={'request': request})

        # Attempt to validate and create the employer instance
        try:
            serializer.is_valid(raise_exception=True)
            employer = serializer.create(serializer.validated_data)
        except ValidationError:
            self.fail('Should not raise ValidationError')

        # Assertions for the created employer instance
        self.assertIsInstance(employer, Employer)
        self.assertEqual(employer.user, self.user)
        self.assertEqual(employer.company_name, data['company_name'])
        self.assertEqual(employer.company_description, data['company_description'])
        self.assertEqual(employer.website, data['website'])