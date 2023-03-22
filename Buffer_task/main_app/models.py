from django.db import models
from authentication.models import User


# Create your models here.

class ItemOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_order = models.CharField(null=True, blank=True, max_length=100)


class Items(models.Model):
    name = models.CharField(max_length=100)

