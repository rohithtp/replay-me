import unittest

from replayer.engine import process_events


class TestProcessEvents(unittest.TestCase):

    def test_work_event(self):
        events = [{'event': 'work', 'company': 'Acme', 'title': 'Engineer',
                   'start_date': '2020-01-01', 'end_date': '2022-12-31'}]
        result = process_events(events)
        self.assertIn('Acme', result)
        self.assertIn('Engineer', result)
        self.assertIn('2020-01-01', result)
        self.assertIn('2022-12-31', result)

    def test_education_event(self):
        events = [{'event': 'education', 'institution': 'MIT', 'degree': 'BS CS',
                   'start_date': '2010-09-01', 'end_date': '2014-06-01'}]
        result = process_events(events)
        self.assertIn('MIT', result)
        self.assertIn('BS CS', result)

    def test_multiple_events_joined_by_newline(self):
        events = [
            {'event': 'work', 'company': 'A', 'title': 'Dev',
             'start_date': '2020-01-01', 'end_date': '2021-01-01'},
            {'event': 'education', 'institution': 'B', 'degree': 'MS',
             'start_date': '2018-01-01', 'end_date': '2020-01-01'},
        ]
        result = process_events(events)
        lines = result.strip().split('\n')
        self.assertEqual(len(lines), 2)

    def test_unknown_event_type_skipped(self):
        events = [{'event': 'award', 'name': 'Best Dev'}]
        result = process_events(events)
        self.assertEqual(result, '')

    def test_empty_events(self):
        self.assertEqual(process_events([]), '')
