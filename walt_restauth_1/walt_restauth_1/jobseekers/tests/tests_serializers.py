from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..serializers import JobseekerSerializer
from ...accounts.serializers import CustomUserCreateSerializer

class JobseekerSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'jobseeker@example.com',
            'password': 'jobseekerpassword',
            'roles': 'jobseeker',
        }

        user_serializer = CustomUserCreateSerializer(data=self.user_data)
        self.assertTrue(user_serializer.is_valid(), user_serializer.errors)
        self.user = user_serializer.save()
        print(self.user)

        self.jobseeker_data = {
            'first_name': 'John',
            'phone_number': '+33612345678',
            'cv': SimpleUploadedFile('cv.pdf', b"cv_file_content", content_type="application/pdf")
        }

        serializer = JobseekerSerializer(data=self.jobseeker_data)
        print(self.jobseeker_data['phone_number'])
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.jobseeker = serializer.save(user_id=self.user.id)

    def test_create_user(self):
        self.assertEqual(self.user.email, 'jobseeker@example.com')
        self.assertEqual(self.user.roles, 'jobseeker')

    def test_create_jobseeker_first_name(self):
        self.assertEqual(self.jobseeker.first_name, 'John')

    # pnone_number: I should not write the unit tests for the packages you install using pip.

    def test_create_jobseeker_cv(self):
        self.assertTrue(self.jobseeker.cv.name.endswith('.pdf'))

    def test_create_jobseeker_user(self):
        self.assertIsNotNone(self.jobseeker)
        self.assertEqual(self.jobseeker.user.id, self.user.id)

