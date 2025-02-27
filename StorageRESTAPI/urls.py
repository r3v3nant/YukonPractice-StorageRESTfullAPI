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
from django.urls import include, path, re_path
#from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from StorageRESTAPI.Storage import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
# router.register(r'productsCategories', views.ProdCategoryViewSet)
# router.register(r'products', views.ProductViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
schema_view = get_schema_view(
    openapi.Info(
        title="Storage API",
        default_version='v1',
        description="API for Storage",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"", views.HomePageView.as_view(), name='main'),

    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),

    path('products/', views.showProductView, name='products'),
    path('products/create', views.create_product, name='createproduct'),
    path('products/<int:product_id>/', views.product_detail, name='readproduct'),
    path('products/<int:product_id>/edit/', views.product_update, name='updateproduct'),
    path('products/<int:product_id>/delete/', views.delete_product, name='deleteproduct'),

    path('productscategories/', views.showProdCategoryView, name='categories'),
    path('productscategories/create', views.create_prodcategory, name='createcategory'),
    path('productscategories/<int:pk>/', views.prodcategory_detail, name='createcategory'),
    path('productscategories/<int:pk>/edit/', views.prodcategory_update, name='updatecategory'),
    path('productscategories/<int:pk>/delete/', views.delete_prodcategory, name='deletecategory'),

    #path('', include(router.urls)),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)