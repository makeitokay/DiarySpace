from django.urls import path

from schools.views import AnnouncementsView

urlpatterns = [
    path("announcements/", AnnouncementsView.as_view(), name='announcements')
]
