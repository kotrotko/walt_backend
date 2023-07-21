from django.test import TestCase
from ..models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(email='testuser1@example.com', password='pass1')
        CustomUser.objects.create_user(email='testuser2@example.com', password='pass2')
        CustomUser.objects.create_user(email='testuser3@example.com', password='pass3')

    def test_filter_by_email(self):
        filtered_users = CustomUser.objects.filter(email__contains='testuser')
        self.assertEqual(filtered_users.count(), 3)

        # The following test is for CustomUser object
        self.assertTrue(CustomUser.objects.filter(email='testuser1@example.com').exists())
