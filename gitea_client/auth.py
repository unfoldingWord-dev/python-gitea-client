"""
Various classes for Gitea authentication
"""
from gitea_client.entities import json_get


class Authentication(object):
    """
    An "abstract" parent class. Represents a
    means of authenticating oneself to Gitea
    """

    def update_kwargs(self, kwargs):
        """
        Updates kwargs to include this object's authentication information
        :param dict kwargs: dictionary of keyword arguments to pass to a function from
            the requests module
        :return: Updated kwargs
        """
        raise NotImplementedError()  # must be implemented by subclasses


class Token(Authentication):
    """
    An immutable representation of a Gitea authentication token
    """

    def __init__(self, token, name=None):
        """
        :param str token: contents of Gitea authentication token
        """
        self._token = token
        self._name = name

    @staticmethod
    def from_json(parsed_json):
        name = json_get(parsed_json, "name")
        sha1 = json_get(parsed_json, "sha1")
        return Token(sha1, name)

    @property
    def name(self):
        """
        The name of the token

        :rtype: str
        """
        return self._name

    @property
    def token(self):
        """
        The contents of the Gitea authentication token

        :rtype: str
        """
        return self._token

    def update_kwargs(self, kwargs):
        if "params" in kwargs:
            kwargs["params"]["token"] = self._token
        else:
            kwargs["params"] = {"token": self._token}


class UsernamePassword(Authentication):
    """
    An immutable representation of a Gitea username/password combination
    """

    def __init__(self, username, password):
        """
        :param str username: Username for Gitea account
        :param str password: Password for Gitea account
        """
        self._username = username
        self._password = password

    @property
    def username(self):
        """
        Username for Gitea account

        :rtype: str
        """
        return self._username

    @property
    def password(self):
        """
        Password for Gitea account
        :rtype: str
        """
        return self._password

    def update_kwargs(self, kwargs):
        kwargs["auth"] = (self._username, self._password)
