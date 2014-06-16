import os

from django.test import TestCase

from .. import import_ical


class ImportIcalTestCase(TestCase):
  fixtures = ['events_test_data.json']

  def setUp(self):
    with file(os.path.dirname(os.path.abspath(__file__)) + '/SampleEvents.ics') as f: s = f.read()
    self.ical_string = s.decode('utf-8')

  def test_events_are_imported(self):
    """events should be imported from icalendar format"""
    imported_events, skipped = import_ical.from_string(self.ical_string)

    self.assertEqual(imported_events.count(), 4)
    self.assertEqual(skipped, 0)


  def test_duplicate_events_are_skipped(self):
    """duplicate events should not be imported"""
    imported_events_1, skipped_1 = import_ical.from_string(self.ical_string)
    imported_events_2, skipped_2 = import_ical.from_string(self.ical_string)

    self.assertEqual(imported_events_1.count(), 4)
    self.assertEqual(skipped_1, 0)
    self.assertEqual(imported_events_2.count(), 0)
    self.assertEqual(skipped_2, 4)


  def test_event_space_name_is_guessed(self):
    """space name should be guessed from ical event location field"""
    imported_events, skipped = import_ical.from_string(self.ical_string)
    test_event = [e for e in imported_events if e.title == 'Some test event'][0]

    self.assertEqual(test_event.space.name == 'Mountain View', True)


  def test_event_functional_areas_are_guessed(self):
    """functional areas should be guessed from ical event description field"""
    imported_events, skipped = import_ical.from_string(self.ical_string)
    test_event = [e for e in imported_events if e.title == 'Some test event'][0]

    self.assertEqual('Security' in test_event.area_names, True)
    self.assertEqual('Firefox OS' in test_event.area_names, True)
