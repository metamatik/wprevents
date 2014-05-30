import urllib2

from django.utils import timezone
from icalendar import Calendar

from wprevents.events.models import Event, Space

default_timezone = timezone.get_default_timezone()


def import_ical(url):
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  data = response.read().decode('utf-8')
  data = data.replace(u"", "") # Temp fix for Mozilla remo ics file

  cal = Calendar.from_ical(data)

  return bulk_create_events(cal)


def bulk_create_events(cal):
  air_mozilla_space = Space.objects.get(name='Air Mozilla')
  events = []

  for ical_event in cal.walk('VEVENT'):
    start = timezone.make_naive(ical_event.get('dtstart').dt, default_timezone)
    end = timezone.make_naive(ical_event.get('dtend').dt, default_timezone)
    title = ical_event.get('summary').encode('utf-8')

    event = Event(
      start = start,
      end = end,
      space = air_mozilla_space,
      title = title,
      description = ical_event.get('description').encode('utf-8')
    )
    # Generate slug because django's bulk_create() does not call Event.save(),
    # which is where an Event's slug is normally set
    event.define_slug()

    events.append(event)

  return Event.objects.bulk_create(events)
