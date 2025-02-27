from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError
import os
# Create your models here.


class ProdCategories(models.Model):
    name = models.CharField(max_length=30, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(ProdCategories, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/products/', null=True)
    preview = models.ImageField(upload_to='media/products/previews/', blank=True, null=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        """Перевизначений метод save() для створення прев’ю"""
        super().save(*args, **kwargs)