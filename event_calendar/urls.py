from django.urls import path
from .views import EventLinkGenerator, DownloadICalendar, PostEvent

urlpatterns = [
    path('', EventLinkGenerator.as_view(), name='index'),
    path('save-links/', EventLinkGenerator.as_view(), name='save_links'),
    path('download-icalendar/<int:event_id>/', DownloadICalendar.as_view(), name='download_icalendar'),
    path('event-post/', PostEvent.as_view(), name='post_event'),
]
