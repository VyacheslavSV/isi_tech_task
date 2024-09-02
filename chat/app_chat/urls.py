from django.urls import path, include
from rest_framework import routers

from .views import ThreadViewSet, MessageViewSet

router = routers.SimpleRouter()

router.register(r'threads', ThreadViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
