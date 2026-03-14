"""
URL configuration for 계급도 (Gyegeupdo) project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connection
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def health_check(request):
    """서버 상태 확인용 헬스체크 엔드포인트"""
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    healthy = db_ok
    data = {
        'status': 'healthy' if healthy else 'unhealthy',
        'database': 'ok' if db_ok else 'error',
    }
    return JsonResponse(data, status=200 if healthy else 503)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', health_check, name='health_check'),

    # API v1 endpoints
    path('api/v1/', include([
        # Auth
        path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('auth/', include('allauth.urls')),

        # App URLs
        path('', include('brands.urls')),
        path('', include('models_app.urls')),
        path('', include('reviews.urls')),
        path('', include('tiers.urls')),
        path('', include('users.urls')),
        path('', include('quiz.urls')),
        path('', include('seo_pages.urls')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
