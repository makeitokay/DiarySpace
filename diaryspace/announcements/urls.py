from django.urls import path

from announcements.views import AnnouncementsView, AnnouncementAddView, AnnouncementEditView

urlpatterns = [
    path("announcements/", AnnouncementsView.as_view(), name='announcements'),
    path("announcements/add/", AnnouncementAddView.as_view(), name='announcement-add'),
    path("announcements/<int:pk>/edit/", AnnouncementEditView.as_view(), name='announcement-edit')
]
