from django.urls import path

from users.views import SchoolAdminCreationView

urlpatterns = [
    path('signup/', SchoolAdminCreationView.as_view(), name='signup'),
]
