import datetime

from django.test import TestCase
from django.conf import settings

from baronbale_website.gc_toolbox.tools import banner_utils


class TestBannerUtils(TestCase):

    def setUp(self):
        try:
            settings.configure()
        except RuntimeError:
            pass

    def test_build_destination_filename_file_ending(self):
        now = datetime.datetime.strptime('22.11.2013 01:23:45', '%d.%m.%Y %H:%M:%S')
        input_file = '/tmp/baronbale/upload.zip'
        file_name = banner_utils.build_destination_filename(input_file, now=now)
        self.assertEqual('20131122_012345.zip', file_name)

    def test_build_destination_filename_no_file_ending(self):
        now = datetime.datetime.strptime('22.11.2013 01:23:45', '%d.%m.%Y %H:%M:%S')
        input_file = '/tmp/baronbale/upload'
        file_name = banner_utils.build_destination_filename(input_file, now=now)
        self.assertEqual('20131122_012345', file_name)

    def test_build_destination_filename_no_input_file(self):
        now = datetime.datetime.strptime('22.11.2013 01:23:45', '%d.%m.%Y %H:%M:%S')
        try:
            banner_utils.build_destination_filename(None, now=now)
            self.fail('TypeError expected')
        except TypeError:
            pass  # Success
