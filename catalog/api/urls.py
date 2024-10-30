from django.urls import path, include
from rest_framework import routers
from catalog.api import views


router = routers.DefaultRouter()
router.register(r'catalogs', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]