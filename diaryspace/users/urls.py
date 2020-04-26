from django.urls import path

from users.views import (
    TeacherAddView,
    TeacherListView,
    ParentListView,
    ParentAddView,
    StudentListView,
    StudentAddView,
)

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teachers/add/", TeacherAddView.as_view(), name="teacher-add"),
    path("parents/", ParentListView.as_view(), name="parents"),
    path("parents/add/", ParentAddView.as_view(), name="parent-add"),
    path("students/", StudentListView.as_view(), name="students"),
    path("students/add/", StudentAddView.as_view(), name="student-add"),
]
