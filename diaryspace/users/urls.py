from django.urls import path

from users.views import TeacherAddView, TeacherListView

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teachers/add/", TeacherAddView.as_view(), name="teacher-add"),
]
