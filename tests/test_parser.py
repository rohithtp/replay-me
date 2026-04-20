import os
import tempfile
import unittest
import yaml

from replayer.parser import parse_events


class TestParseEvents(unittest.TestCase):

    def _write(self, data):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(data, f)
        f.close()
        return f.name

    def tearDown(self):
        pass  # individual tests clean up their own files

    def test_valid_list(self):
        path = self._write([{'event': 'work', 'company': 'Acme'}])
        try:
            events = parse_events(path)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]['company'], 'Acme')
        finally:
            os.unlink(path)

    def test_multiple_events(self):
        data = [
            {'event': 'work', 'company': 'A'},
            {'event': 'education', 'institution': 'MIT'},
        ]
        path = self._write(data)
        try:
            events = parse_events(path)
            self.assertEqual(len(events), 2)
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        events = parse_events('/nonexistent/path/events.yaml')
        self.assertEqual(events, [])

    def test_invalid_yaml_not_a_list(self):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        f.write('key: value\n')
        f.close()
        try:
            with self.assertRaises(ValueError):
                parse_events(f.name)
        finally:
            os.unlink(f.name)

    def test_empty_file(self):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        f.write('')
        f.close()
        try:
            with self.assertRaises(ValueError):
                parse_events(f.name)
        finally:
            os.unlink(f.name)
