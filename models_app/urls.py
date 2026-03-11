from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, PostViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]
