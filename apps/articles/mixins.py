from django.contrib.auth.views import redirect_to_login


class RedirectNotAuthUser:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(request.path)
        return super().dispatch(request, *args, **kwargs)
