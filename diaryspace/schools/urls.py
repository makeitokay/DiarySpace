from django.urls import path

from schools.views import AnnouncementsView, AnnouncementAddView

urlpatterns = [
    path("announcements/", AnnouncementsView.as_view(), name='announcements'),
    path("announcements/add/", AnnouncementAddView.as_view(), name='announcement-add')
]
