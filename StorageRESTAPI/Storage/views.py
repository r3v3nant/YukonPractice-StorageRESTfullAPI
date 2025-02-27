from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #для виведення повідомлень на сторінці
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from .models import ProdCategories, Products
from .forms import ProductForm, ProdCategoryForm

# from .permissions import IsOwnerOrReadOnly
# from rest_framework import permissions, viewsets
# from StorageRESTAPI.Storage.serializers import UserSerializer, ProductSerializer, ProdCategorySerializer

def login_user(request):
    if request.method == "POST":
        userlogin = request.POST["login"]
        userpassword = request.POST["password"]
        user = authenticate(request, username=userlogin, password=userpassword)
        if user is not None:
            login(request, user)
            return redirect('main')

        else:
            messages.success(request, ("Wrong login data"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

@login_required
def logout_user(request):
    logout(request)
    return redirect('main')

class HomePageView(TemplateView):
    template_name = 'index.html'
    context_object_name = 'main page'

@login_required
def showProdCategoryView(request):
    categories = ProdCategories.objects.all()
    return render(request, 'productscategories.html', {'categories': categories})

@login_required
def create_prodcategory(request):
    if request.method == "POST":
        form = ProdCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = ProdCategoryForm()
    return render(request, 'createProductscategories.html', {'form': form})


@login_required
def prodcategory_detail(request, pk):
    category = get_object_or_404(ProdCategories, pk=pk)
    return render(request, 'readProductscategories.html', {'category': category})

@login_required
def prodcategory_update(request, pk):
    category = get_object_or_404(ProdCategories, pk=pk)
    if request.method == "POST":
        form = ProdCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = ProdCategoryForm(instance=category)
    return render(request, 'updateProductscategories.html', {'form': form})

@login_required
def delete_prodcategory(request, pk):
    category = get_object_or_404(ProdCategories, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('categories')
    return render(request, 'deleteProductscategories.html', {'category': category})

@login_required
def showProductView(request):
    products = Products.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
#CREATE (Створення нового продукту)
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user  # Прив’язуємо до поточного користувача
            product.save()
            return redirect('products')  # Переадресація на список продуктів
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        form = ProductForm()

    return render(request, 'createProduct.html', {'form': form})

#Read
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if product is None:
        messages.success(request, ("Product is no longer valid!"))
        return redirect('products')
    form = ProductForm(instance=product)
    messages.success(request, ("You can`t modify that product!"))
    return render(request, 'readProduct.html', {'form': form, 'product': product})


# Update
@login_required
def product_update(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if product is None:
        messages.success(request, ("Product is no longer valid!"))
        return redirect('products')

    form = ProductForm(instance=product)
    if product.created_by != request.user:
        messages.success(request, ("You can`t modify that product!"))
        return product_detail(request, product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, ("Product successfully modified"))
            return redirect('products')
    else:
        return render(request, 'updateProduct.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    # Перевіряємо, чи користувач є автором продукту
    if product.created_by != request.user:
        messages.success(request, ("You can`t delete that product!"))
        return redirect('products')

    if request.method == "POST":
        product.delete()
        return redirect('products')

    return render(request, 'deleteProduct.html', {'product': product})