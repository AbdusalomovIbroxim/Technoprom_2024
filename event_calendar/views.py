from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from icalendar import Calendar, Event

from .models import EventLink


class EventLinkGenerator(View):

    @staticmethod
    def get(request):
        return render(request, 'calendar/index.html')

    def post(self, request):
        if self.request.method == 'POST':
            title = self.request.POST.get('event-title')
            description = self.request.POST.get("event-description")
            start_date = self.request.POST.get("event-start-date")
            end_date = self.request.POST.get("event-end-date")
            location = self.request.POST.get("event-location")

            start_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

            google_calendar_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&dates={start_datetime}/{end_datetime}&details={description}&location={location}&text={title}"

            event_link = EventLink.objects.create(
                title=title,
                description=description,
                location=location,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                google_calendar_link=google_calendar_link
            )

            download_url = reverse('download_icalendar', kwargs={'event_id': event_link.pk})

            return JsonResponse({'message': 'Links and file saved successfully.', "id": event_link.pk,
                                 "google_calendar_link": google_calendar_link,
                                 'download_ics_link': request.build_absolute_uri(download_url),
                                 'event_id': event_link.pk, }
                                )


class DownloadICalendar(View):
    @staticmethod
    def get(request, event_id):
        try:
            event_link = EventLink.objects.get(pk=event_id)
        except EventLink.DoesNotExist:
            return HttpResponse("EventLink does not exist", status=404)

        cal = Calendar()
        event = Event()
        event.add('summary', event_link.title)
        event.add('description', event_link.description)
        event.add('location', event_link.location)
        event.add('dtstart', event_link.start_datetime)
        event.add('dtend', event_link.end_datetime)
        event.add('dtstamp', event_link.start_datetime)
        event.add('uid', str(event_link.pk))
        cal.add_component(event)

        icalendar_data = cal.to_ical()

        response = HttpResponse(icalendar_data, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="event_{event_link.pk}.ics"'
        return response

class PostEvent(View):
    @staticmethod
    def get(request):
        return render(request, 'calendar/create_event.html')
