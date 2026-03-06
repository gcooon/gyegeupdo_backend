from django.urls import path
from .views import seo_landing

urlpatterns = [
    path('seo/landing/', seo_landing, name='seo-landing'),
]
