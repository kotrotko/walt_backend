from django.db import models
from moses.models import CustomUser
from walt.accounts.models import Company

class Job(models.Model):
    company_name = models.ForeignKey(Company, related_name='Company', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=300)
    job_description = models.RichTextField()
    salary = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.job_title}'


class Application(models.Model):
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cv/')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

