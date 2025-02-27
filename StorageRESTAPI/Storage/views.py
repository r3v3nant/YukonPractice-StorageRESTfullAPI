from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #для виведення повідомлень на сторінці
from django.contrib.auth.decorators import login_required

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# from django.contrib.auth.models import User
from .models import ProdCategories, Products
from .forms import ProductForm, ProdCategoryForm, ProductFilterForm

# from .permissions import IsOwnerOrReadOnly
# from rest_framework import permissions, viewsets
# from StorageRESTAPI.Storage.serializers import UserSerializer, ProductSerializer, ProdCategorySerializer


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD)
        },
        required=['username', 'password']
    ),
    responses={200: "Success", 400: "Invalid credentials"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для роботи з формою
@permission_classes([AllowAny])
def login_user(request):
    if request.method == "POST":
        userlogin = request.POST.get("login")
        password = request.POST.get("password")

        if not userlogin or not password:
            messages.error(request, "Введіть логін і пароль")
            return redirect("login")  # Перенаправлення назад на сторінку входу

        user = authenticate(request, username=userlogin, password=password)
        if user is not None:
            login(request, user)
            return redirect("main")  # Перенаправлення на головну сторінку
        else:
            messages.error(request, "Невірний логін або пароль")
            return redirect("login")

    # GET-запит – відображає сторінку входу
    return render(request, "login.html")

@swagger_auto_schema(
    method='post',
    operation_description="Logout the user and return a JSON response",
    responses={200: "Logged out successfully", 401: "Unauthorized"}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)

class HomePageView(TemplateView):
    template_name = 'index.html'
    context_object_name = 'main page'

@permission_classes([IsAuthenticated])
def showProdCategoryView(request):
    categories = ProdCategories.objects.all()
    return render(request, 'productscategories.html', {'categories': categories})


@swagger_auto_schema(
    method='post',
    operation_description="Create a new product category",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Category name"),
        },
        required=['name']
    ),
    responses={201: "Category created", 400: "Invalid data"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для роботи з формою
@permission_classes([IsAuthenticated])
def create_prodcategory(request):
    if request.method == "POST":
        form = ProdCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
        else:
            return render(request, 'createProductscategories.html', {'form': form, 'error': "Invalid data"})

    # GET-запит – відображає сторінку та форму
    form = ProdCategoryForm()
    return render(request, 'createProductscategories.html', {'form': form})


@swagger_auto_schema(
    method='get',
    operation_description="Get details of a specific product category",
    responses={200: "Category details", 404: "Category not found"}
)
@api_view(["GET"])# Додаємо GET для відкриття сторінки
@permission_classes([IsAuthenticated])
def prodcategory_detail(request, pk):
    category = get_object_or_404(ProdCategories, pk=pk)
    return render(request, 'readProductscategories.html', {'category': category})


@swagger_auto_schema(
    method='post',
    operation_description="Update an existing product category",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Updated category name"),
        },
        required=['name']
    ),
    responses={200: "Category updated", 400: "Invalid data", 404: "Category not found"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для роботи з формою
@permission_classes([IsAuthenticated])
def prodcategory_update(request, pk):
    category = get_object_or_404(ProdCategories, pk=pk)

    if request.method == "POST":  # Використовуємо POST замість PUT
        form = ProdCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')  # Після оновлення перенаправляємо на список категорій
        else:
            return Response({"error": "Invalid data"}, status=400)

    # Якщо метод GET – рендеримо сторінку
    form = ProdCategoryForm(instance=category)
    return render(request, 'updateProductscategories.html', {'form': form, 'category': category})


@swagger_auto_schema(
    method='post',  # Використовуємо POST замість DELETE для форм
    operation_description="Delete a product category",
    responses={204: "Category deleted", 404: "Category not found"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для видалення
@permission_classes([IsAuthenticated])
def delete_prodcategory(request, pk):
    category = get_object_or_404(ProdCategories, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect('categories')  # Після видалення перенаправляємо на сторінку категорій

    return render(request, 'deleteProductscategories.html', {'category': category})



@permission_classes([IsAuthenticated])
def showProductView(request): # Сторінка продуктів

    products = Products.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():     # Форма-фільтр
        search_query = form.cleaned_data.get("search")
        if search_query:
            products = products.filter(name__icontains=search_query)

        category = form.cleaned_data.get("category")
        if category:
            products = products.filter(category=category)

    return render(request, "products.html", {"products": products, "form": form})

# CREATE (Створення нового продукту)
@swagger_auto_schema(
    method='post',
    operation_description="Create a new product",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Product name"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Product description"),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Product price"),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format="binary", description="Product image"),
        },
        required=['name', 'price']
    ),
    responses={201: "Product created", 400: "Invalid data"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для роботи з формою
@permission_classes([IsAuthenticated])
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('products')
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")

    # GET-запит → Повертаємо порожню форму
    form = ProductForm()
    return render(request, 'createProduct.html', {'form': form})


# READ (Перегляд продукту)
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a product by ID",
    responses={200: "Product details", 404: "Product not found"}
)
@api_view(["GET"])  # Додаємо GET для відкриття сторінки
@permission_classes([IsAuthenticated])
def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    form = ProductForm(instance=product)
    return render(request, 'readProduct.html', {'form': form, 'product': product})


# UPDATE (Оновлення продукту)
@swagger_auto_schema(
    method='post',
    operation_description="Update a product",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Updated product name"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Updated product description"),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Updated product price"),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format="binary", description="Updated product image"),
        },
        required=['name', 'price']
    ),
    responses={200: "Product updated", 403: "Not authorized", 404: "Product not found"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для роботи з формою
@permission_classes([IsAuthenticated])
def product_update(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if product.created_by != request.user: # Якщо інший користувач створив продукт, то переадресовуємо його на сторінку перегляду продукту
        messages.error(request, "You can’t modify this product!")
        return redirect('readproduct', product_id=product.id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully modified")
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'updateProduct.html', {'form': form, 'product': product})


# DELETE (Видалення продукту)
@swagger_auto_schema(
    method='post',
    operation_description="Delete a product",
    responses={204: "Product deleted", 403: "Not authorized", 404: "Product not found"}
)
@api_view(["GET", "POST"])  # Додаємо GET для відкриття сторінки, POST для видалення
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if product.created_by != request.user:
        messages.error(request, "You can’t delete this product!")
        return redirect('products')

    if request.method == "POST":
        product.delete()
        return redirect('products')

    # GET-запит – відкриває сторінку підтвердження видалення
    return render(request, 'deleteProduct.html', {'product': product})