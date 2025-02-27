"""
URL configuration for StorageRESTAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
#from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static



from StorageRESTAPI.Storage import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
# router.register(r'productsCategories', views.ProdCategoryViewSet)
# router.register(r'products', views.ProductViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"", views.HomePageView.as_view(), name='main'),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('products/', views.showProductView, name='products'),
    path('products/create', views.create_product, name='createproduct'),
    path('products/<int:product_id>/', views.product_update, name='readproduct'),
    path('products/<int:product_id>/edit/', views.product_update, name='updateproduct'),
    path('products/<int:product_id>/delete/', views.delete_product, name='deleteproduct'),
    path('productscategories/', views.showProdCategoryView, name='categories'),
    path('productscategories/create', views.create_prodcategory, name='createcategory'),
    path('productscategories/<int:pk>/', views.prodcategory_detail, name='createcategory'),
    path('productscategories/<int:pk>/edit/', views.prodcategory_update, name='updatecategory'),
    path('productscategories/<int:pk>/delete/', views.delete_prodcategory, name='deletecategory'),
    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)