from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound


class SystemLoginRequiredMixin(LoginRequiredMixin):
    """Mixin that checks user has `school_id` attribute to access school pages"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.school is None:
            return HttpResponseNotFound()
        return super().dispatch(request, *args, **kwargs)
