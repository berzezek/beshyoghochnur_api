from django.urls import path, include
from rest_framework import routers
from catalog.api import views


router = routers.DefaultRouter()
router.register(r'catalog', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]