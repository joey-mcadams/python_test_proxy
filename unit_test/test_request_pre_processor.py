from unittest import TestCase
from util.request_pre_processor import is_invalid_key_present, is_repeat_request
from config.config import BAD_KEY
import logging


class MockRequest():
    def __init__(self, data):
        self.data = data.encode()


class MockRequest2():
    def __init__(self, url, origin, data):
        self.data = data
        self.base_url = url
        self.remote_addr = origin


class TestRequestPreProcessor(TestCase):
    def setUp(self):
        self.bad_json_string = f'{{ "{BAD_KEY}": true }}'
        self.bad_json_string2 = f'{{ "hidden": {{ "{BAD_KEY}": true }} }}'
        self.bad_json_object_in_list_in_object = f'{{ "hidden": [{{ "{BAD_KEY}": true }}] }}'
        self.bad_json_object_in_list = f'["good_value", "good_value", {{ "{BAD_KEY}": true }}]'
        self.good_json_string = '{ "something": "not malicious" }'
        self.good_json_string_empty_key = '{ "data": null }'
        self.good_string = "This is a string: is_malicious"
        self.good_json_string_empty = '{}'
        self.good_payload_empty = None

##############################
# is_invalid_key_present Tests
##############################

    def test_invalid_key_present_in_list(self):
        test_request = MockRequest(self.bad_json_object_in_list)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertTrue(result)


    def test_invalid_key_present_in_list(self):
        test_request = MockRequest(self.bad_json_object_in_list_in_object)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertTrue(result)

    def test_invalid_key_present_good_string(self):
        test_request = MockRequest(self.good_string)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertFalse(result)

    def test_invalid_key_present_bad_json(self):
        test_request = MockRequest(self.bad_json_string)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertTrue(result)

    def test_invalid_key_present_bad_json2(self):
        test_request = MockRequest(self.bad_json_string2)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertTrue(result)

    def test_invalid_key_present_good_json(self):
        test_request = MockRequest(self.good_json_string)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertFalse(result)

    def test_invalid_key_present_good_json_string_empty(self):
        test_request = MockRequest(self.good_json_string_empty)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertFalse(result)

    def test_invalid_key_present_good_empty_payload(self):
        test_request = MockRequest("")
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertFalse(result)

    def test_invalid_key_present_good_empty_key(self):
        test_request = MockRequest(self.good_json_string_empty_key)
        result = is_invalid_key_present(test_request)
        logging.info(result)
        self.assertFalse(result)

##############################
# is_repeat_request Tests
##############################
    def test_is_repeat_request(self):
        test_request = MockRequest2("http://www.google.com", "0.0.0.0", "")
        self.assertTrue(is_repeat_request(test_request, test_request))

    def test_is_repeat_request_mismatched_data(self):
        test_request = MockRequest2("http://www.google.com", "0.0.0.0", "")
        test_last_request = MockRequest2("http://www.google.com", "0.0.0.0", "some_data")
        self.assertFalse(is_repeat_request(test_request, test_last_request))

    def test_is_repeat_request_mismatched_origin(self):
        test_request = MockRequest2("http://www.google.com", "0.0.0.0", "")
        test_last_request = MockRequest2("http://www.google.com", "0.0.0.1", "")
        self.assertFalse(is_repeat_request(test_request, test_last_request))

    def test_is_repeat_request_mismatched_url(self):
        test_request = MockRequest2("http://www.google.com", "0.0.0.0", "")
        test_last_request = MockRequest2("http://google.com", "0.0.0.0", "")
        self.assertFalse(is_repeat_request(test_request, test_last_request))
