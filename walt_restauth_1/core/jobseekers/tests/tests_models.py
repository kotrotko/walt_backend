from django.test import TestCase
from ...accounts.models import CustomUser
from ..models import JobSeeker

class DatabaseTestCase(TestCase):

    def test_database_operations(self):
        # Create a new user and jobseeker record
        user = CustomUser.objects.create(email='user@foo.com')
        jobseeker = JobSeeker.objects.create(user=user, first_name='John', phone_number='+95673407225')

        # Retrieve the created jobseeker record from the database
        retrieved_jobseeker = JobSeeker.objects.get(user=user)
        self.assertEqual(retrieved_jobseeker, jobseeker)

        # Update the jobseeker record
        jobseeker.first_name = 'Updated Name'
        jobseeker.save()

        # Retrieve the updated jobseeker recors from the database
        updated_jobseeker = JobSeeker.objects.get(id=jobseeker.id)
        self.assertEqual(updated_jobseeker.first_name, 'Updated Name')

        # Delete the jobseeker record
        jobseeker.delete()

        # Make sure the record is no longer in the database
        with self.assertRaises(JobSeeker.DoesNotExist):
            JobSeeker.objects.get(id=jobseeker.id)



