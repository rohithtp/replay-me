import os
import sys
import tempfile
import unittest
import yaml
from io import StringIO
from unittest.mock import patch

from replayer.cli import main


WORK = {
    'event': 'work', 'company': 'Sample Company', 'title': 'Software Engineer',
    'start_date': '2023-01-01', 'end_date': '2023-12-31',
}


def _write_yaml(data):
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    f.close()
    return f.name


class TestCLIReplayFlow(unittest.TestCase):

    def setUp(self):
        self.events_file = _write_yaml([dict(WORK)])

    def tearDown(self):
        if os.path.exists(self.events_file):
            os.unlink(self.events_file)

    def _run(self, argv):
        with patch('sys.argv', argv), \
             patch('sys.stdout', new_callable=StringIO) as mock_out:
            try:
                main()
            except SystemExit:
                pass
            return mock_out.getvalue()

    # --- replay <file> ---

    def test_replay_prints_company(self):
        out = self._run(['replay', self.events_file])
        self.assertIn('Sample Company', out)

    def test_replay_prints_title(self):
        out = self._run(['replay', self.events_file])
        self.assertIn('Software Engineer', out)

    def test_replay_missing_file(self):
        out = self._run(['replay', '/no/such/file.yaml'])
        self.assertIn('No valid events found', out)

    # --- replay add-event ---

    def test_add_event_work(self):
        path = tempfile.mktemp(suffix='.yaml')
        try:
            out = self._run([
                'replay', 'add-event', path,
                'event=work', 'company=NewCo', 'title=Dev',
                'start_date=2024-01-01', 'end_date=2024-12-31',
            ])
            self.assertIn('added at index 0', out)
            with open(path) as f:
                events = yaml.safe_load(f)
            self.assertEqual(events[0]['company'], 'NewCo')
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_add_event_missing_fields_prints_error(self):
        out = self._run(['replay', 'add-event', self.events_file, 'event=work'])
        self.assertIn('Error', out)

    def test_add_event_too_few_args_prints_usage(self):
        out = self._run(['replay', 'add-event', self.events_file])
        self.assertIn('Usage', out)

    def test_add_event_invalid_kv_format_exits(self):
        with patch('sys.argv', ['replay', 'add-event', self.events_file, 'badarg']), \
             self.assertRaises(SystemExit):
            main()

    # --- replay update-event ---

    def test_update_event_changes_field(self):
        out = self._run([
            'replay', 'update-event', self.events_file, '0', 'title=Lead Engineer',
        ])
        self.assertIn('Lead Engineer', out)
        with open(self.events_file) as f:
            events = yaml.safe_load(f)
        self.assertEqual(events[0]['title'], 'Lead Engineer')

    def test_update_event_out_of_range_prints_error(self):
        out = self._run(['replay', 'update-event', self.events_file, '99', 'title=X'])
        self.assertIn('Error', out)

    def test_update_event_non_integer_index_prints_error(self):
        out = self._run(['replay', 'update-event', self.events_file, 'abc', 'title=X'])
        self.assertIn('Index must be an integer', out)

    def test_update_event_too_few_args_prints_usage(self):
        out = self._run(['replay', 'update-event', self.events_file, '0'])
        self.assertIn('Usage', out)

    # --- replay --help ---

    def test_help_flag(self):
        out = self._run(['replay', '--help'])
        self.assertIn('Commands', out)

    def test_no_args_prints_help(self):
        out = self._run(['replay'])
        self.assertIn('Commands', out)


if __name__ == '__main__':
    unittest.main()
