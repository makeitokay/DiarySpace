from django.shortcuts import render
from django.views import View


class AnnouncementsView(View):
    def get(self, request):
        return render(request, 'announcements.html')
