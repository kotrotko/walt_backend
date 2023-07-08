from django.db import models

from ..accounts.models import CustomUser


class Employer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employer', limit_choices_to={'roles': 'employer'})
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    website = models.URLField(max_length=200)

    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"

    def __str__(self):
        return f'{self.company_name}'
