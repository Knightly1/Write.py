import unittest
from write import Write
from io import StringIO
from contextlib import contextmanager
from unittest.mock import patch
import re
import datetime

@contextmanager
def does_not_raise():
    yield

class TestWrite(unittest.TestCase):
    def setUp(self):
        self.stdout = StringIO()
        self.log = Write(use_colors=False, log_level='trace', stream=self.stdout)

    def tearDown(self):
        self.log = None
        self.stdout.seek(0)  # move to the start of the file
        self.stdout.truncate(0)  # clear the file content

    def _get_output(self):
        output = self.stdout.getvalue().strip()
        output = output.rstrip('\x1b[0m')  # strip the ANSI reset code at the end of the line from color log
        return output

    def test_trace(self):
        self.log.trace('test trace')
        output = self._get_output()
        self.assertIn('TRACE :: test trace', output)

    def test_debug(self):
        self.log.debug('test debug')
        output = self._get_output()
        self.assertIn('DEBUG :: test debug', output)

    def test_info(self):
        self.log.info('test info')
        output = self._get_output()
        self.assertIn('INFO  :: test info', output)

    def test_warn(self):
        self.log.warn('test warn')
        output = self._get_output()
        self.assertIn('WARN  :: test warn', output)

    def test_error(self):
        self.log.error('test error')
        output = self._get_output()
        self.assertIn('ERROR :: test error', output)

    def test_fatal(self):
        with patch('sys.exit', return_value=None):
            self.log.fatal('test fatal')
        output = self._get_output()
        self.assertIn('FATAL :: test fatal', output)

    def test_help(self):
        self.log.help('test help')
        output = self._get_output()
        self.assertIn('HELP  :: test help', output)

    def test_trace_logging(self):
        with self.assertLogs('write', level='TRACE') as cm:
            self.log.trace("test trace")
            self.assertIn('TRACE:write:test trace', cm.output[0])

    def test_debug_logging(self):
        with self.assertLogs('write', level='DEBUG') as cm:
            self.log.debug("test debug")
            self.assertIn('DEBUG:write:test debug', cm.output[0])

    def test_info_logging(self):
        with self.assertLogs('write', level='INFO') as cm:
            self.log.info("test info")
            self.assertIn('INFO:write:test info', cm.output[0])

    def test_warn_logging(self):
        with self.assertLogs('write', level='WARN') as cm:
            self.log.warn("test warn")
            self.assertIn('WARN:write:test warn', cm.output[0])

    def test_error_logging(self):
        with self.assertLogs('write', level='ERROR') as cm:
            self.log.error("test error")
            self.assertIn('ERROR:write:test error', cm.output[0])

    def test_fatal_logging(self):
        with self.assertRaises(SystemExit):
            with self.assertLogs('write', level='FATAL') as cm:
                self.log.fatal("test fatal")
                self.assertIn('FATAL:write:test fatal', cm.output[0])

    def test_help_logging(self):
        with self.assertLogs('write', level='HELP') as cm:
            self.log.help("test help")
            self.assertIn('HELP:write:test help', cm.output[0])

    def test_colors(self):
        self.log = Write(use_colors=True, log_level='trace', stream=self.stdout)
        self.log.trace('test trace')
        output = self._get_output()
        # Regular expression for ANSI escape codes.
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.assertRegex(output, ansi_escape)

    def test_log_level(self):
        self.log = Write(use_colors=False, log_level='debug', stream=self.stdout)
        self.log.trace('test trace')
        output = self._get_output()
        self.assertNotIn('trace', output)

    def test_format_string(self):
        fmt_string='%(message)s'
        self.log = Write(use_colors=False, log_level='trace', stream=self.stdout, format_string=fmt_string)
        self.log.trace('test trace')
        output = self._get_output()
        self.assertEqual('test trace', output)

    def test_date_format(self):
        date_fmt = '%Y-%m-%d %I:%M:%S %p'
        self.log = Write(use_colors=False, log_level='trace', stream=self.stdout, date_format=date_fmt)
        self.log.trace('test trace')
        output = self._get_output()
        # Extract date string from output
        date_string = output.split('::')[0].strip()
        # Try to create datetime object from date string. If it fails, the format is incorrect.
        datetime.datetime.strptime(date_string, date_fmt)

if __name__ == '__main__':
    unittest.main()