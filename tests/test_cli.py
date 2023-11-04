import unittest

from curler import get_curl_cli_parsed_args


class TestCLI(unittest.TestCase):
    def test_curl_command(self):
        curl = "bad http://example.com"
        self.assertRaises(AssertionError, get_curl_cli_parsed_args, curl)


if __name__ == "__main__":
    unittest.main()
