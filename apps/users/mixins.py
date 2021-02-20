from django.http.response import HttpResponseRedirect


class RedirectAuthUser:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_redirect_url()
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
