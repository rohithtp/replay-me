import unittest
from replayer.cli import main

class TestSampleFlow(unittest.TestCase):
    def test_sample_event(self):
        # Define a sample event for testing
        sample_event = {
            "event": "work",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "company": "Sample Company",
            "title": "Software Engineer"
        }

        # Run the main function with the sample event
        result = main(sample_event)

        # Assert that the output is as expected
        self.assertIn("Sample Company", result)
        self.assertIn("Software Engineer", result)

if __name__ == '__main__':
    unittest.main()
