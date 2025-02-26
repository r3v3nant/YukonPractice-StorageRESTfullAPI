from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProdCategories(models.Model):
    name = models.CharField(max_length=30, unique=True)

    objects = models.Manager()



class Products(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(ProdCategories, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
