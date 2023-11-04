import unittest

from curler import typing
from curler.parser import parse_curl


class TestCurlParser(unittest.TestCase):
    def test_get_request(self):
        curl_command = "curl http://example.com"
        parsed = parse_curl(curl_command)
        self.assertEqual(parsed.method, typing.http_method.GET)

    def test_post_request(self):
        curl_command = 'curl -X POST -d "data" http://example.com'
        parsed = parse_curl(curl_command)
        self.assertEqual(parsed.method, "POST")

    def test_cookies_and_headers(self):
        curl_command = """curl \
            -H "Cookie: cookie1=value1; cookie2=value2" \
            -H "Authorization: Bearer token" \
            -H "Content-Type: application/json" \
            http://example.com"""
        parsed = parse_curl(curl_command)
        self.assertEqual(parsed.cookies, {"cookie1": "value1", "cookie2": "value2"})
        self.assertEqual(
            parsed.headers,
            {
                "Authorization": "Bearer token",
                "Content-Type": "application/json",
            },
        )

    def test_proxy_and_user_auth(self):
        curl_command = """curl \
            -x proxy.example.com:8080 \
            -U user:password \
            http://example.com"""
        parsed = parse_curl(curl_command)
        self.assertEqual(parsed.user, ("user", "password"))
        self.assertEqual(
            parsed.proxy,
            {
                "http": "http://user:password@proxy.example.com:8080/",
                "https": "https://user:password@proxy.example.com:8080/",
            },
        )

    def test_not_implemented_method(self):
        curl_command = "curl -X PUT http://example.com"
        self.assertRaises(NotImplementedError, parse_curl, curl_command)

    def test_for_requests_method(self):
        command = "curl https://example.com"
        parsed = parse_curl(command).for_requests
        self.assertIsInstance(parsed, dict)
        self.assertListEqual(
            list(parsed.keys()),
            ["method", "url"],
            "Check ordering of the list elements.",
        )
        self.assertEqual(parsed["url"], "https://example.com")
        self.assertEqual(parsed["method"], typing.http_method.GET)


if __name__ == "__main__":
    unittest.main()
