import unittest

from recursive_json_search import *
from test_data import *


class json_search_test(unittest.TestCase):

    def test_search_found(self):
        """Key should be found, return list should not be empty."""
        self.assertTrue([] != json_search(key1, data))

    def test_search_not_found(self):
        """Key should not be found, should return an empty list."""
        self.assertTrue([] == json_search(key2, data))

    def test_is_a_list(self):
        """Search result should be a list."""
        self.assertIsInstance(json_search(key1, data), list)

    def test_viewer_cannot_read_api_key(self):
        """Viewer must not be able to read apiKey."""
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual([], result)

    def test_operator_cannot_read_api_key(self):
        """Operator must not be able to read apiKey."""
        result = json_search("apiKey", data, role="operator")
        self.assertEqual([], result)

    def test_admin_can_read_api_key(self):
        """Admin must be allowed to read apiKey."""
        result = json_search("apiKey", data, role="admin")
        self.assertNotEqual([], result)

    def test_viewer_cannot_read_management_ip(self):
        """Viewer must not be able to read managementIpAddress."""
        result = json_search(
            "managementIpAddress",
            data,
            role="viewer"
        )
        self.assertEqual([], result)

    def test_operator_can_read_management_ip(self):
        """Operator must be allowed to read managementIpAddress."""
        result = json_search(
            "managementIpAddress",
            data,
            role="operator"
        )
        self.assertNotEqual([], result)


if __name__ == '__main__':
    unittest.main() 