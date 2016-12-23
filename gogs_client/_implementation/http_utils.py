"""
Various HTTP utilities
"""

import requests
from future.moves.urllib.parse import urljoin


class RelativeHttpRequestor(object):
    """
    A thin wrapper around the requests module that allows for endpoint paths
    to be given relative to a fixed base URL
    """
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = session or requests.Session()

    def absolute_url(self, relative_path):
        """
        :param str relative_path: relative URL
        :return: absolute URL of relative_path, relative to this object's base URL
        :rtype: str
        """
        return append_url(self.base_url, relative_path)

    # The below methods are identical to the corresponding functions in requests module,
    # except that they expect relative paths

    def delete(self, relative_path, **kwargs):
        return self.session.delete(self.absolute_url(relative_path), **kwargs)

    def get(self, relative_path, params=None, **kwargs):
        return self.session.get(self.absolute_url(relative_path), params=params, **kwargs)

    def options(self, relative_path, params=None, **kwargs):
        return self.session.options(self.absolute_url(relative_path), params=params, **kwargs)

    def patch(self, relative_path, data=None, **kwargs):
        return self.session.patch(self.absolute_url(relative_path), data=data, **kwargs)

    def post(self, relative_path, data=None, **kwargs):
        return self.session.post(self.absolute_url(relative_path), data=data, **kwargs)

    def put(self, relative_path, params=None, data=None, **kwargs):
        return self.session.put(self.absolute_url(relative_path), params=params, data=data, **kwargs)


def append_url(base_url, path):
    """
    Append path to base_url in a sensible way.
    """
    if base_url[-1] != "/":
        base_url += "/"
    if path[0] == "/":
        path = path[1:]
    return urljoin(base_url, path)
