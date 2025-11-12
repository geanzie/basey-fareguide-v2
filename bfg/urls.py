"""
URL configuration for bfg project - Basey Fare Guide API
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# Import ViewSets
from users.views import (
    UserViewSet, VehicleViewSet, DiscountCardViewSet,
    DiscountUsageLogViewSet, IncidentViewSet, FareCalculationViewSet
)
from users import auth_views
from locations.views import LocationViewSet
from routes.views import RouteViewSet, calculate_route
from fares.views import FareViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'discount-cards', DiscountCardViewSet, basename='discountcard')
router.register(r'discount-usage-logs', DiscountUsageLogViewSet, basename='discountusagelog')
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'fare-calculations', FareCalculationViewSet, basename='farecalculation')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'fares', FareViewSet, basename='fare')

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Authentication endpoints
    path('v2/auth/register/', auth_views.register_user, name='register'),
    path('v2/auth/login/', auth_views.login_user, name='login'),
    path('v2/auth/logout/', auth_views.logout_user, name='logout'),
    path('v2/auth/me/', auth_views.get_current_user, name='current-user'),
    path('v2/auth/profile/', auth_views.update_user_profile, name='update-profile'),
    path('v2/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Route calculation endpoint
    path('v2/routes/calculate/', calculate_route, name='calculate-route'),
    
    # API routes from router
    path('v2/', include(router.urls)),
]

# Media files (for development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve React App - catch-all pattern (should be last)
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='react-app'),
]
