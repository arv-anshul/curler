import unittest

from curler.parser import curl_command_parser
from curler.typing import ParsedCurl


class TestCurlParser(unittest.TestCase):
    def test_get_request(self):
        curl_command = "curl http://example.com"
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(method="GET", url="http://example.com")
        self.assertEqual(parsed, expected)

    def test_post_request(self):
        curl_command = 'curl -X POST -d "data" http://example.com'
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(method="POST", url="http://example.com", data="data")
        self.assertEqual(parsed, expected)

    def test_custom_headers(self):
        curl_command = 'curl -H "Content-Type: application/json" -H "Authorization: Bearer token" http://example.com'
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(
            method="GET",
            url="http://example.com",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer token",
            },
        )
        self.assertEqual(parsed, expected)

    def test_cookies_and_headers(self):
        curl_command = 'curl -H "Cookie: cookie1=value1; cookie2=value2" -H "Authorization: Bearer token" http://example.com'
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(
            method="GET",
            url="http://example.com",
            headers={"Authorization": "Bearer token"},
            cookies={"cookie1": "value1", "cookie2": "value2"},
        )
        self.assertEqual(parsed, expected)

    def test_proxy_and_user_auth(self):
        curl_command = (
            "curl -x proxy.example.com:8080 -U user:password http://example.com"
        )
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(
            method="GET",
            url="http://example.com",
            user=("user", "password"),
            proxy={
                "http": "http://user:password@proxy.example.com:8080/",
                "https": "https://user:password@proxy.example.com:8080/",
            },
        )
        self.assertEqual(parsed, expected)

    def test_not_implemented_method(self):
        curl_command = "curl -X PUT http://example.com"
        self.assertRaises(NotImplementedError, curl_command_parser, curl_command)


if __name__ == "__main__":
    unittest.main()
