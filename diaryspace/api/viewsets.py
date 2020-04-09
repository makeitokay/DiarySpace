from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin

from schools.models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin):
    queryset = Announcement.objects.none()  # Required for DjangoModelPermissions
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        group = self.request.user.group
        return Announcement.objects.filter(groups=group)
