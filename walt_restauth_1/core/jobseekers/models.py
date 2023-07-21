from django.db import models

from ..accounts.models import CustomUser

from phonenumber_field.modelfields import PhoneNumberField

class JobSeeker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='job_seekers', limit_choices_to={'roles': 'jobseeker'})
    first_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(max_length=100)
    cv = models.FileField()

    class Meta:
        verbose_name = "Job Seeker"
        verbose_name_plural = "Job Seekers"

    def __str__(self):
        return f'{self.first_name}'

    @property
    def email(self):
        return self.user.email