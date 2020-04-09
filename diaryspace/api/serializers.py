from rest_framework.serializers import ModelSerializer

from schools.models import Announcement


class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id"]
