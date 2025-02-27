from django.db import models
from django.contrib.auth.models import User # Підключення моделі користувачів

class ProdCategories(models.Model): # Модель категорій продуктів
    name = models.CharField(max_length=30, unique=True)

    objects = models.Manager()

    def __str__(self):   # Повертає ім'я замість id/primarykey
        return self.name


class Products(models.Model): # Модель продуктів
    name = models.CharField(max_length=30)
    category = models.ForeignKey(ProdCategories, on_delete=models.CASCADE)  # Підастановка значень з категорій
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)          # Підастановка значень з користувачів
    image = models.ImageField(upload_to='media/products/', null=True)
    preview = models.ImageField(upload_to='media/products/previews/', blank=True, null=True)

    objects = models.Manager()