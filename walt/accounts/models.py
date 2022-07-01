from django.db import models
import moses
from moses.models import CustomUser

class Company(models.Model):
    company_name = models.CharField(CustomUser)
    first_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    phone_number = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Applicant(models.Model):
    first_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

