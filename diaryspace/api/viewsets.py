from rest_framework.mixins import DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from announcements.models import Announcement
from api.serializers import AnnouncementSerializer


class AnnouncementViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin):
    queryset = Announcement.objects.none()  # Required for DjangoModelPermissions
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        group = self.request.user.group
        return Announcement.objects.filter(groups=group)
