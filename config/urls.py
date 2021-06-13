import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("", include("apps.articles.urls")),
    path("", include("apps.users.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
