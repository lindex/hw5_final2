from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts import views

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
path('sentry-debug/', trigger_error),
    path('404/', views.page_not_found, name='404'),
    path('500/', views.server_error, name='500'),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("adminpanel/", admin.site.urls),
    path("", include("posts.urls")),
    path("", include("about.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
