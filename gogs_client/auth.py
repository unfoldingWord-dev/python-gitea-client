"""
Various classes for Gogs authentication
"""


class GogsAuthentication(object):
    """
    An "abstract" parent class for GogsAuthentication objects. Represents a
    means of authenticating oneself to Gogs
    """
    def update_kwargs(self, kwargs):
        """
        Updates kwargs to include this object's authentication information
        :param kwargs: dictionary of keyword arguments to pass to a function from
            the requests module
        :return: Updated kwargs
        """
        raise NotImplementedError()  # must be implemented by subclasses


class GogsToken(GogsAuthentication):
    def __init__(self, token):
        self._token = token

    @property
    def token(self): return self._token

    def update_kwargs(self, kwargs):
        if "params" in kwargs:
            kwargs["params"]["token"] = self._token
        else:
            kwargs["params"] = {"token": self._token}


class GogsUsernamePassword(GogsAuthentication):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def username(self): return self._username

    @property
    def password(self): return self._password

    def update_kwargs(self, kwargs):
        kwargs["auth"] = (self._username, self._password)
