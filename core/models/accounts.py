from django.contrib.auth.models import AbstractUser
from django.db import models

class Client(models.Model):

    user = models.OneToOneField('core.User', on_delete=models.CASCADE)

    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='clients/logo/', blank=True, null=True)

    official_email = models.EmailField()
    phone = models.CharField(max_length=20)

    poc_name = models.CharField(max_length=255, blank=True, null=True)
    poc_email = models.EmailField(blank=True, null=True)
    poc_phone = models.CharField(max_length=20, blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    gstin = models.CharField(max_length=50, blank=True, null=True)

    website = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"