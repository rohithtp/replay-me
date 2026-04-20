import os
import tempfile
import unittest
import yaml

from replayer.creator import add_event, update_event


WORK = {
    'event': 'work', 'company': 'Acme', 'title': 'Engineer',
    'start_date': '2020-01-01', 'end_date': '2022-12-31',
}

EDUCATION = {
    'event': 'education', 'institution': 'MIT', 'degree': 'BS CS',
    'start_date': '2010-09-01', 'end_date': '2014-06-01',
}


class TestAddEvent(unittest.TestCase):

    def setUp(self):
        self.f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        self.f.close()
        self.path = self.f.name

    def tearDown(self):
        os.unlink(self.path)

    def _load(self):
        with open(self.path) as f:
            return yaml.safe_load(f) or []

    def test_add_work_event_to_empty_file(self):
        idx = add_event(self.path, dict(WORK))
        self.assertEqual(idx, 0)
        events = self._load()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['company'], 'Acme')

    def test_add_education_event(self):
        idx = add_event(self.path, dict(EDUCATION))
        self.assertEqual(idx, 0)
        events = self._load()
        self.assertEqual(events[0]['institution'], 'MIT')

    def test_add_multiple_events_increments_index(self):
        idx0 = add_event(self.path, dict(WORK))
        idx1 = add_event(self.path, dict(EDUCATION))
        self.assertEqual(idx0, 0)
        self.assertEqual(idx1, 1)
        self.assertEqual(len(self._load()), 2)

    def test_add_to_nonexistent_file_creates_it(self):
        os.unlink(self.path)
        add_event(self.path, dict(WORK))
        self.assertTrue(os.path.exists(self.path))
        self.assertEqual(len(self._load()), 1)

    def test_missing_required_field_raises(self):
        bad = {'event': 'work', 'company': 'Acme'}  # missing title, dates
        with self.assertRaises(ValueError):
            add_event(self.path, bad)

    def test_unknown_event_type_raises(self):
        with self.assertRaises(ValueError):
            add_event(self.path, {'event': 'award', 'name': 'Best Dev'})

    def test_file_not_modified_on_validation_failure(self):
        add_event(self.path, dict(WORK))
        with self.assertRaises(ValueError):
            add_event(self.path, {'event': 'work'})  # missing fields
        self.assertEqual(len(self._load()), 1)  # unchanged


class TestUpdateEvent(unittest.TestCase):

    def setUp(self):
        self.f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        self.f.close()
        self.path = self.f.name
        add_event(self.path, dict(WORK))
        add_event(self.path, dict(EDUCATION))

    def tearDown(self):
        os.unlink(self.path)

    def _load(self):
        with open(self.path) as f:
            return yaml.safe_load(f) or []

    def test_update_single_field(self):
        event = update_event(self.path, 0, {'title': 'Senior Engineer'})
        self.assertEqual(event['title'], 'Senior Engineer')
        self.assertEqual(self._load()[0]['title'], 'Senior Engineer')

    def test_update_preserves_other_fields(self):
        update_event(self.path, 0, {'title': 'Lead'})
        saved = self._load()[0]
        self.assertEqual(saved['company'], 'Acme')
        self.assertEqual(saved['start_date'], '2020-01-01')

    def test_update_second_event(self):
        update_event(self.path, 1, {'degree': 'MS CS'})
        self.assertEqual(self._load()[1]['degree'], 'MS CS')

    def test_update_out_of_range_raises(self):
        with self.assertRaises(IndexError):
            update_event(self.path, 99, {'title': 'X'})

    def test_update_negative_index_raises(self):
        with self.assertRaises(IndexError):
            update_event(self.path, -1, {'title': 'X'})

    def test_update_removing_required_field_raises(self):
        with self.assertRaises(ValueError):
            update_event(self.path, 0, {'company': ''})
