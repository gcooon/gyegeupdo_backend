from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, home_summary

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('brands', BrandViewSet, basename='brand')

urlpatterns = [
    path('home/summary/', home_summary, name='home-summary'),
    path('', include(router.urls)),
]
