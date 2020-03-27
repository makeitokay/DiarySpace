from django.urls import path
from .views import management_home_view

urlpatterns = [
    path('', management_home_view, name='home')
]
