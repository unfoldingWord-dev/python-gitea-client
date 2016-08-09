import unittest

import gogs_client._implementation.http_utils as http_utils


class HttpUtilsTest(unittest.TestCase):

    def test_append_url1(self):
        base = "https://www.google.com/"
        path = "/images/"
        self.assertEqual(http_utils.append_url(base, path), "https://www.google.com/images/")

    def test_append_url2(self):
        base = "http://www.hello.world.net"
        path = "great/api/v1"
        self.assertEqual(http_utils.append_url(base, path), "http://www.hello.world.net/great/api/v1")

    def test_append_url3(self):
        base = "https://hello.org/dir1/dir2"
        path = "/dir3/file.txt"
        self.assertEqual(http_utils.append_url(base, path),
                         "https://hello.org/dir1/dir2/dir3/file.txt")

    def test_absolute1(self):
        base = "https://www.google.com/"
        path = "/images/"
        requestor = http_utils.RelativeHttpRequestor(base)
        self.assertEqual(requestor.absolute_url(path), "https://www.google.com/images/")

    def test_absolute2(self):
        base = "http://www.hello.world.net"
        path = "great/api/v1"
        requestor = http_utils.RelativeHttpRequestor(base)
        self.assertEqual(requestor.absolute_url(path), "http://www.hello.world.net/great/api/v1")

    def test_absolute3(self):
        base = "https://hello.org/dir1/dir2"
        path = "/dir3/file.txt"
        requestor = http_utils.RelativeHttpRequestor(base)
        self.assertEqual(requestor.absolute_url(path),
                         "https://hello.org/dir1/dir2/dir3/file.txt")

if __name__ == "__main__":
    unittest.main()
