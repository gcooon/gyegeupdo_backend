from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TierDisputeViewSet, TrendViewSet, UserTierChartViewSet

router = DefaultRouter()
router.register('disputes', TierDisputeViewSet, basename='dispute')
router.register('trends', TrendViewSet, basename='trend')
router.register('user-charts', UserTierChartViewSet, basename='user-chart')

urlpatterns = [
    path('tiers/', include(router.urls)),
]
