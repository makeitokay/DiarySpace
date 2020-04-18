from django.urls import path

from users.views import TeacherListView

urlpatterns = [
    path('teachers/', TeacherListView.as_view(), name='teachers'),
]