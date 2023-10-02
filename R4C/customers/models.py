from django.db import models
from django.core.validators import RegexValidator

class Customer(models.Model):
    email = models.CharField(max_length=255, blank=False, null=False, validators=[RegexValidator(regex='^[A-Za-z0-9.]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$')])
