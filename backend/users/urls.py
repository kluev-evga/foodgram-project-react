from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]