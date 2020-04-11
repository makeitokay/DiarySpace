from django.urls import path

from diaryspace_auth.views import SchoolAdminCreationView

urlpatterns = [
    path('signup/', SchoolAdminCreationView.as_view(), name='signup'),
]
