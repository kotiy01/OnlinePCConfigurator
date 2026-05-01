"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from components.views import CPUViewSet, GPUViewSet, MotherboardViewSet, RAMViewSet, StorageViewSet, CaseViewSet, PowerSupplyViewSet, CPUCoolerViewSet, CaseFanViewSet, compatibility_check
from prices.views import ShopItemViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from components.views_auth import RegisterView, LoginView, LogoutView, ProfileView, SavedBuildListCreateView, SavedBuildRetrieveUpdateDestroyView, PublicBuildView

router = DefaultRouter()
router.register(r'cpu', CPUViewSet, basename='cpu')
router.register(r'gpu', GPUViewSet)
router.register(r'motherboard', MotherboardViewSet)
router.register(r'ram', RAMViewSet)
router.register(r'storage', StorageViewSet)
router.register(r'case', CaseViewSet)
router.register(r'psu', PowerSupplyViewSet)
router.register(r'cooler', CPUCoolerViewSet)
router.register(r'casefan', CaseFanViewSet)

router.register(r'prices', ShopItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/check-compatibility/', compatibility_check, name='compatibility_check'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    path('api/saved-builds/', SavedBuildListCreateView.as_view(), name='saved-builds'),
    path('api/saved-builds/<int:pk>/', SavedBuildRetrieveUpdateDestroyView.as_view(), name='saved-build-detail'),
    path('api/public-build/<int:build_id>/', PublicBuildView.as_view(), name='public-build'),
]
