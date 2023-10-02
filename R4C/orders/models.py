from django.db import models
from R4C.customers.models import Customer
from R4C.robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=9,blank=False, null=False)
