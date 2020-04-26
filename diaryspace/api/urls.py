from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import AnnouncementViewSet

router = DefaultRouter()
router.register("announcements", AnnouncementViewSet, "announcement")

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("", include(router.urls)),
]
