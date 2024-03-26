from uuid import uuid4
from django.db.models import (Model,
                              TextField,
                              CharField,
                              DateTimeField,
                              URLField,
                              BooleanField,
                              ImageField,
                              UUIDField,
                              ForeignKey, CASCADE, )


class EventLink(Model):
    title = CharField(max_length=100)
    description = TextField()
    location = CharField(max_length=255)
    start_datetime = DateTimeField(auto_now_add=True)
    end_datetime = DateTimeField(auto_now_add=True)
    google_calendar_link = URLField()
    map_link = URLField(blank=True, null=True)
    unique_id = UUIDField(default=uuid4, editable=False, unique=True)
    is_published = BooleanField(default=False)

    def __str__(self):
        return self.title


class Images(Model):
    photo = ImageField(upload_to='event_photos/', blank=True, null=True)
    event = ForeignKey(EventLink, CASCADE)
