from django.urls import include, path
from rest_framework import routers

from api.views import index, CustomUserViewSet

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('index/', index),
    # path('/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]