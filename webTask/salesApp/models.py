from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Items(models.Model):
    itemImage = models.ImageField(upload_to="images", height_field=None, width_field=None, max_length=100, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=100000)
    totalSoldProduct = models.BigIntegerField(default=0)
    productPrice = models.FloatField()
    uploadDate = models.BigIntegerField(null=True)
    IID = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)

    class Meta:
        ordering = ("-uploadDate",)


# ------------------------------------------------- Accounts Model ------------------------------------------------- #
class CustomUser(AbstractUser):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images", height_field=None, width_field=None, max_length=100, blank=True)
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    email = models.EmailField(max_length=200)


# ---------------------------------------------- Company receipts---------------------------------------------- #
class Receipts(models.Model):
    seller = models.CharField(max_length=100, blank=True)
    buyer = models.CharField(max_length=100, blank=True)
    product = models.CharField(max_length=100)
    notes = models.TextField(max_length=100000)
    price = models.FloatField()
    datetime = models.BigIntegerField(null=True)
    RID = models.BigAutoField(primary_key=True)

    class Meta:
        ordering = ("-datetime",)
