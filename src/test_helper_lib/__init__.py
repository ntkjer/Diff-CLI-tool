import unittest
import click_datetime
import datetime as dt
from datetime import datetime

from helper_lib import *
from requests.exceptions import HTTPError


class TestHelperLib(unittest.TestCase):

    def setUp(self):
        self.path = '/tmp/ehub_data'
        ts = '2016-01-01T03:00:00'
        ts_format ='%Y-%m-%dT%H:%M:%S'
        ts = datetime.strptime(ts, ts_format)
        self.ts_valid = ts
        self.top_dir_valid = make_top_dir(self.ts_valid, self.path)
        self.dir_valid = make_dir(self.ts_valid, self.path)
        self.file_valid = make_file_from_time(self.ts_valid, self.path)
        ts = '2017-01-01T03:00:00'
        ts_format ='%Y-%m-%dT%H:%M:%S'
        ts = datetime.strptime(ts, ts_format)
        self.ts_invalid = ts


    def test_download_S3(self):
        # self.assertEqual(download_S3('s3://net.energyhub.assets/public/dev-exercises/audit-data/'), './tmp/')

        # with self.assertRaises(requests.exceptions.HTTPError):
        #     download_S3('s3://net.energyhub.assets/public/dev-exercises/path/does/not/exist')
        pass

    def test_validate_date(self):
        pass


    def test_build_state(self):
        pass


    def test_get_state(self):
        pass


    def test_retrieve_fields(self):
        pass


    def test_select_closest_bound(self):
        pass


    def test_make_dir(self):
        self.assertEqual(make_dir(self.ts_valid, self.path), self.dir_valid)


    def test_make_file_from_time(self):
        self.assertEqual(make_file_from_time(self.ts_valid, self.path), self.file_valid)


    def test_make_top_dir(self):
        self.assertEqual(make_top_dir(self.ts_valid, self.path), self.top_dir_valid)


    def test_does_file_exist(self):
        ts = '2016-01-01T03:00:00'
        ts_format ='%Y-%m-%dT%H:%M:%S'
        ts = datetime.strptime(ts, ts_format)
        self.assertEqual(does_file_exist(self.ts_valid), True)
        self.assertEqual(does_file_exist(self.ts_invalid), False)


    def test_get_boundary_data(self):
        d = {'high': '{"changeTime": "2016-01-01T03:02:30.001424", "after": {"ambientTemp": 78.0}, "before": {"ambientTemp": 77.0}}\n', 'low_delta': dt.timedelta(0, 749, 997587), 'low': '{"changeTime": "2016-01-01T02:47:30.002413", "after": {"ambientTemp": 77.0}, "before": {"ambientTemp": 79.0}}\n', 'high_delta': dt.timedelta(0, 150, 1424)}
        path = '/tmp/ehub_data/2016/01/01.jsonl.gz'
        self.assertEqual(get_boundary_data(self.ts, path), d)


    def test_sanitize_date(self):
        self.assertEqual(sanitize_date(1), "01")
        self.assertEqual(sanitize_date(12), "12")
        self.assertEqual(sanitize_date(0), "00")
        with self.assertRaises(ValueError):
            sanitize_date(1000)
            sanitize_date(None)


    def test_sanitize_dates(self):
        self.assertEqual(sanitize_dates(12, 1), ("12", "01"))
        self.assertEqual(sanitize_dates(1, 1), ("01", "01"))
        self.assertEqual(sanitize_dates(1, 1), ("01", "01"))
        with self.assertRaises(ValueError):
            sanitize_dates(20, 32)


    def test_sanitize_integer(self):
        self.assertEqual(sanitize_integer(1), "01")
        self.assertEqual(sanitize_integer(12), "12")
        self.assertEqual(sanitize_integer(0), "00")
        with self.assertRaises(ValueError):
            sanitize_integer(1000)
            sanitize_integer(None)


    

if __name__ == '__main__':
    unittest.main()