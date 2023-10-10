import unittest

from curler import curl_command_parser
from curler.constants import Method
from curler.typing import ParsedCurl

http_method = Method()


class TestCurlCommands(unittest.TestCase):
    def test_curl_command_1(self):
        curl_command = (
            "curl 'https://pypi.python.org/pypi/uncurl' "
            """--data '[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]' """
            "-H 'Accept-Encoding: gzip,deflate,sdch' "
            "-H 'Cookie: foo=bar; baz=baz2'"
        )
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(
            method="GET",
            url="https://pypi.python.org/pypi/uncurl",
            data='[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]',
            headers={
                "Accept-Encoding": "gzip,deflate,sdch",
            },
            cookies={"foo": "bar", "baz": "baz2"},
        )
        self.assertEqual(parsed, expected)

    def test_curl_command_2(self):
        curl_command = (
            "curl 'https://pypi.python.org/pypi/uncurl' "
            """--data '{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}' """
            "-H 'Accept-Encoding: gzip,deflate,sdch' "
            "-H 'Cookie: foo=bar; baz=baz2'"
        )
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(
            method="GET",
            url="https://pypi.python.org/pypi/uncurl",
            data='{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}',
            headers={
                "Accept-Encoding": "gzip,deflate,sdch",
            },
            cookies={"foo": "bar", "baz": "baz2"},
        )
        self.assertEqual(parsed, expected)

    def test_curl_command_3(self):
        curl_command = (
            "curl 'https://pypi.python.org/pypi/uncurl' "
            "--data 'this is just some data'"
        )
        parsed = curl_command_parser(curl_command)
        self.assertEqual(parsed.method, http_method.GET)

    def test_curl_command_4(self):
        curl_command = (
            "curl 'https://pypi.python.org/pypi/uncurl' "
            "-X 'POST' "
            "--data-binary 'this is just some data'"
        )
        parsed = curl_command_parser(curl_command)

        self.assertEqual(parsed.method, http_method.POST)
        self.assertEqual(parsed.data_binary, "this is just some data")

    def test_curl_command_5(self):
        curl_command = (
            "curl "
            "'http://pandahomeios.ifjing.com/action.ashx/otheraction/9028' "
            "-H 'PID: 20000079' "
            "-H 'MT: 4' "
            "-H 'DivideVersion: 1.0' "
            "-H 'SupPhone: Redmi Note 3' "
            "-H 'SupFirm: 5.0.2' "
            "-H 'IMEI: wx_app' "
            "-H 'IMSI: wx_app' "
            "-H 'SessionId: ' "
            "-H 'CUID: wx_app' "
            "-H 'ProtocolVersion: 1.0' "
            "-H 'Sign: 7876480679c3cfe9ec0f82da290f0e0e' "
            "-H 'Accept: /' "
            "-H 'BodyEncryptType: 0' "
            """-H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({"packageName":"com.oppo.market","type":"other","extra":{}})' """
            "-H 'Content-Type: text/plain; charset=utf-8' "
            "-H 'Host: pandahomeios.ifjing.com' "
            """--data-binary '{"CateID":"508","PageIndex":1,"PageSize":30}' """
            "--compressed"
        )
        parsed = curl_command_parser(curl_command)
        expected = ParsedCurl(
            method="POST",
            url="http://pandahomeios.ifjing.com/action.ashx/otheraction/9028",
            data_binary='{"CateID":"508","PageIndex":1,"PageSize":30}',
            headers={
                "PID": "20000079",
                "MT": "4",
                "DivideVersion": "1.0",
                "SupPhone": "Redmi Note 3",
                "SupFirm": "5.0.2",
                "IMEI": "wx_app",
                "IMSI": "wx_app",
                "SessionId": "",
                "CUID": "wx_app",
                "ProtocolVersion": "1.0",
                "Sign": "7876480679c3cfe9ec0f82da290f0e0e",
                "Accept": "/",
                "BodyEncryptType": "0",
                "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({"packageName":"com.oppo.market","type":"other","extra":{}})',
                "Content-Type": "text/plain; charset=utf-8",
                "Host": "pandahomeios.ifjing.com",
            },
            compressed=True,
        )
        self.assertEqual(parsed, expected)

    def test_curl_command_7(self):
        curl_command = (
            "curl 'https://pypi.python.org/pypi/uncurl' "
            "-H 'Accept-Encoding: gzip,deflate' "
            "--insecure"
        )
        parsed = curl_command_parser(curl_command)
        self.assertEqual(parsed.insecure, True)

    def test_curl_command_8(self):
        curl_command = (
            "curl 'https://pypi.python.org/pypi/uncurl' "
            r"-H $'cookie: sid=00Dt00000004XYz\u0021ARg'"
        )
        parsed = curl_command_parser(curl_command)
        self.assertEqual(parsed.cookies, {"sid": "00Dt00000004XYz!ARg"})


if __name__ == "__main__":
    unittest.main()
