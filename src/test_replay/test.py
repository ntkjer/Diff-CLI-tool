import click
import unittest
from replay import cli
from helper_lib import clear_local_file as clear

from click.testing import CliRunner


class TestReplay(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.expected_output = ""

    def test_replay_help(self):
        runner = self.runner
        result = runner.invoke(
            cli,
            ["--help"]
        )
        self.assertEqual(0, result.exit_code)
        self.assertIn("NAME", result.output)
        self.assertIn("SYNOPSIS", result.output)
        self.assertIn("DESCRIPTION", result.output)
        self.assertIn("EXAMPLES", result.output)


    def test_replay_input_args(self):
        runner = self.runner
        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '-f', 'schedule', 'alice', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = "Invalid entry"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "Usage: replay --help"
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['-f', 'ambientTemp', 'alice', 'bob']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = "Error: Invalid value"
        self.assertIn(self.expected_output, result.output)

  

    def test_replay_local_path(self):
        runner = self.runner
        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '/tmp/ehub_data', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0}}'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', '/tmp/ehub_data', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0, "schedule": "false"}}'
        self.assertIn(self.expected_output, result.output)        

        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', '/tmp/ehub_data/', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0, "schedule": "false"}}'
        self.assertIn(self.expected_output, result.output)
 
        result = runner.invoke(
            cli,
            ['-f', 'ambientTemp', '--field', 'schedule', '/tmp/ehub_data/', '2016-01-01']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = "Error: Invalid value"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "does not match format '%Y-%m-%dT%H:%M"
        self.assertIn(self.expected_output, result.output)
        
        result = runner.invoke(
            cli,
            ['-f', 'ambientTemp', '--field', 'schedule', '/tmp/ehub_data/', '2016-05-22T09:17', 'auspicious_arg']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = "Error: Got unexpected extra argument"
        self.assertIn(self.expected_output, result.output)
 
        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', '/this/is/a/bogus/path', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = "Invalid entry"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "Usage: replay --help"
        self.assertIn(self.expected_output, result.output)

       
        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', '/tmp/ehub_data', '2017-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = "Invalid entry"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "Usage: replay --help"
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--field', 'smell', '/tmp/ehub_data', '2016-01-01T03:00']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = 'Error: Invalid value for "--field" / "-f": invalid choice: smell. (choose from schedule, ambientTemp, heatTemp)'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['---field', 'smell', '/tmp/ehub_data', '2016-01-01T03:00']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = 'Error: no such option: ---field'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--an_option', 'option', '/tmp/ehub_data', '2016-01-01T03:00']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = 'Error: no such option:'
        self.assertIn(self.expected_output, result.output)
        #Use different fields

  
    def test_replay_s3(self):
        runner = self.runner

        clear('/tmp/ehub_data')
        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0, "schedule": "false"}}'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0}}'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0, "schedule": "false"}}'
        self.assertIn(self.expected_output, result.output)        

        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = '{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0, "schedule": "false"}}'
        self.assertIn(self.expected_output, result.output)
 
        result = runner.invoke(
            cli,
            ['-f', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = "Error: Invalid value"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "does not match format '%Y-%m-%dT%H:%M"
        self.assertIn(self.expected_output, result.output)
        
        result = runner.invoke(
            cli,
            ['-f', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-05-22T09:17', 'auspicious_arg']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = "Error: Got unexpected extra argument"
        self.assertIn(self.expected_output, result.output)
 
        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/but/the/path/is/wrong', '2016-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = "Invalid entry"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "Usage: replay --help"
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--field', 'ambientTemp', '--field', 'schedule', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2017-01-01T03:00']
        )
        self.assertEqual(0, result.exit_code)
        self.expected_output = "Invalid entry"
        self.assertIn(self.expected_output, result.output)
        self.expected_output = "Usage: replay --help"
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--field', 'smell', 's3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01T03:00']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = 'Error: Invalid value for "--field" / "-f": invalid choice: smell. (choose from schedule, ambientTemp, heatTemp)'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['---field', 'smell', '/tmp/ehub_data', '2016-01-01T03:00']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = 'Error: no such option: ---field'
        self.assertIn(self.expected_output, result.output)

        result = runner.invoke(
            cli,
            ['--an_option', 'option','s3://net.energyhub.assets/public/dev-exercises/audit-data/', '2016-01-01T03:00']
        )
        self.assertEqual(2, result.exit_code)
        self.expected_output = 'Error: no such option:'
        self.assertIn(self.expected_output, result.output)
        #Use different fields


if __name__ == "__main__":
    unittest.main()