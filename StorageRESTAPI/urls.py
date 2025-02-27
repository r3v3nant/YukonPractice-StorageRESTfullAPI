from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from StorageRESTAPI.Storage import views

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
    path(r"", views.HomePageView.as_view(), name='main'),                                   # Головна сторінка

    path('login_user', views.login_user, name='login'),                                     # Сторінка входу
    path('logout_user', views.logout_user, name='logout'),                                  # Функція виходу

    path('products/', views.showProductView, name='products'),                              # Сторінка всіх продуктів
    path('products/create', views.create_product, name='createproduct'),                    # Сторінка створення продуктів
    path('products/<int:product_id>/', views.product_detail, name='readproduct'),           # Сторінка перегляду продукту
    path('products/<int:product_id>/edit/', views.product_update, name='updateproduct'),    # Сторінка оновлення продукту
    path('products/<int:product_id>/delete/', views.delete_product, name='deleteproduct'),  # Сторінка видалення продукту

    #Відповідні сторінки для категорій
    path('productscategories/', views.showProdCategoryView, name='categories'),
    path('productscategories/create', views.create_prodcategory, name='createcategory'),
    path('productscategories/<int:pk>/', views.prodcategory_detail, name='createcategory'),
    path('productscategories/<int:pk>/edit/', views.prodcategory_update, name='updatecategory'),
    path('productscategories/<int:pk>/delete/', views.delete_prodcategory, name='deletecategory'),

    #SwaggerDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Додавання шляху для картинок