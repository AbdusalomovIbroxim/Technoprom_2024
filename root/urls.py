from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language

urlpatterns = [
    path(_("admin/"), admin.site.urls),
    path("", include("films.urls")),
    path("users/", include("accounts.urls")),
    path("support/", include("support.urls")),
    path("accounts/", include("allauth.urls")),
    path("linkpro/", include("event_calendar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("films.urls")),
    path("users/", include("accounts.urls")),
    path("linkpro/", include("event_calendar.urls")),
)

# -------------------------------------------------------------------------------------------
