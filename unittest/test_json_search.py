import unittest

from recursive_json_search import *
from test_data import *


class json_search_test(unittest.TestCase):

    def test_search_found(self):
        expected = [{key1: "Network Device 10.10.20.82 Is Unreachable From Controller"}]
        self.assertEqual(expected, json_search(key1, data, role="viewer"))

    def test_search_not_found(self):
        self.assertEqual([], json_search(key2, data, role="viewer"))

    def test_is_a_list(self):
        self.assertIsInstance(json_search(key1, data), list)

    def test_search_aggregates_nested_dict_and_list_matches(self):
        nested_data = {
            "level1": {
                "target": "first",
                "items": [{"target": "second"}, ["ignored", {"target": "third"}]],
            }
        }
        self.assertEqual(
            [{"target": "first"}, {"target": "second"}, {"target": "third"}],
            json_search("target", nested_data),
        )

    def test_viewer_cannot_search_nested_api_key(self):
        self.assertEqual([], json_search("apiKey", data, role="viewer"))

    def test_operator_cannot_search_nested_api_key(self):
        self.assertEqual([], json_search("apiKey", data, role="operator"))

    def test_admin_can_search_nested_api_key(self):
        self.assertEqual(
            [{"apiKey": "SNMP-COMMUNITY-STRING-7f3a9c"}],
            json_search("apiKey", data, role="admin"),
        )

    def test_viewer_cannot_search_management_ip(self):
        self.assertEqual([], json_search("managementIpAddress", data, role="viewer"))

    def test_operator_can_search_management_ip(self):
        self.assertEqual(
            [{"managementIpAddress": "10.10.20.21"}],
            json_search("managementIpAddress", data, role="operator"),
        )

    def test_viewer_can_search_issue_summary(self):
        self.assertEqual(
            [{key1: "Network Device 10.10.20.82 Is Unreachable From Controller"}],
            json_search(key1, data, role="viewer"),
        )


if __name__ == '__main__':
    unittest.main() 
