from .models import ProdCategories, Products
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class ProdCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProdCategories
        fields = ['url', 'name']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ['url', 'name', 'category', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user  # Додаємо авторизованого користувача
        return super().create(validated_data)