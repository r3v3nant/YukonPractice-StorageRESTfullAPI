from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from .models import ProdCategories, Products
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions, viewsets

from StorageRESTAPI.Storage.serializers import UserSerializer, ProductSerializer, ProdCategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProdCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProdCategories.objects.all()
    serializer_class = ProdCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
