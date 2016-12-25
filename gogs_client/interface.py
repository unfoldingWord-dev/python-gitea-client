import requests

from gogs_client._implementation.http_utils import RelativeHttpRequestor, append_url
from gogs_client.entities import GogsUser, GogsRepo
from gogs_client.auth import Token


class GogsApi(object):
    """
    A Gogs client, serving as a wrapper around the Gogs HTTP API.
    """

    def __init__(self, base_url, session=None):
        """
        :param str base_url: the URL of the Gogs server to communicate with. Should be given
                             with the https protocol
        :param str session: a requests session instance
        """
        api_base = append_url(base_url, "/api/v1/")
        self._requestor = RelativeHttpRequestor(api_base, session=session)

    def valid_authentication(self, auth):
        """
        Returns whether ``auth`` is valid

        :param auth.Authentication auth: authentication object
        :return: whether the provided authentication is valid
        :rtype: bool
        :raises NetworkFailure: if there is an error communicating with the server
        """
        return self._get("/user", auth=auth).ok

    def authenticated_user(self, auth):
        """
        Returns the user authenticated by ``auth``

        :param auth.Authentication auth: authentication for user to retrieve

        :return: user authenticated by the provided authentication
        :rtype: GogsUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        response = self._get("/user", auth=auth)
        return GogsUser.from_json(self._check_ok(response).json())

    def get_tokens(self, auth, username=None):
        """
        Returns the tokens owned by the specified user. If no user is specified,
        uses the user authenticated by ``auth``.

        :param auth.Authentication auth: authentication for user to retrieve.
        Must be a username-password authentication, due to a restriction of the
        Gogs API
        :param str username: username of owner of tokens

        :return: list of tokens
        :rtype: List[Token]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        if username is None:
            username = self.authenticated_user(auth).username
        response = self._get("/users/{u}/tokens".format(u=username), auth=auth)
        return [Token.from_json(o) for o in self._check_ok(response).json()]

    def create_token(self, auth, name, username=None):
        """
        Creates a new token with the specified name for the specified user.
        If no user is specified, uses user authenticated by ``auth``.

        :param auth.Authentication auth: authentication for user to retrieve.
        Must be a username-password authentication, due to a restriction of the
        Gogs API
        :param str name: name of new token
        :param str username: username of owner of new token

        :return: new token representation
        :rtype: Token
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        if username is None:
            username = self.authenticated_user(auth).username
        data = {"name": name}
        response = self._post("/users/{u}/tokens".format(u=username), auth=auth, data=data)
        return Token.from_json(self._check_ok(response).json())

    def ensure_token(self, auth, name, username=None):
        """
        Ensures the existence of a token with the specified name for the
        specified user. Creates a new token if none exists. If no user is
        specified, uses user authenticated by ``auth``.

        :param auth.Authentication auth: authentication for user to retrieve.
        Must be a username-password authentication, due to a restriction of the
        Gogs API
        :param str name: name of new token
        :param str username: username of owner of new token

        :return: token representation
        :rtype: Token
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        if username is None:
            username = self.authenticated_user(auth).username
        tokens = [token for token in self.get_tokens(auth, username) if token.name == name]
        if tokens:
            return tokens[0]
        return self.create_token(auth, name, username)

    def create_repo(self, auth, name, description=None, private=False, auto_init=False,
                    gitignore_templates=None, license_template=None, readme_template=None):
        """
        Creates a new repository, and returns the created repository.

        :param auth.Authentication auth: authentication object
        :param str name: name of the repository to create
        :param str description: description of the repository to create
        :param bool private: whether the create repository should be private
        :param bool auto_init: whether the created repository should be auto-initialized with an initial commit
        :param list[str] gitignore_templates: collection of ``.gitignore`` templates to apply
        :param str license_template: license template to apply
        :param str readme_template: README template to apply
        :return: a representation of the created repository
        :rtype: GogsRepo
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        gitignores = None if gitignore_templates is None \
            else ",".join(gitignore_templates)
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
            "gitignores": gitignores,
            "license": license_template,
            "readme": readme_template
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        response = self._post("/user/repos", auth=auth, data=data)
        return GogsRepo.from_json(self._check_ok(response).json())

    def repo_exists(self, auth, username, repo_name):
        """
        Returns whether a repository with name ``repo_name`` owned by the user with username ``username`` exists.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: name of repository
        :return: whether the repository exists
        :rtype: bool
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}".format(u=username, r=repo_name)
        return self._get(path, auth=auth).ok

    def get_repo(self, auth, username, repo_name):
        """
        Returns a the repository with name ``repo_name`` owned by
        the user with username ``username``.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: name of repository
        :return: a representation of the retrieved repository
        :rtype: GogsRepo
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}".format(u=username, r=repo_name)
        response = self._check_ok(self._get(path, auth=auth))
        return GogsRepo.from_json(response.json())

    def delete_repo(self, auth, username, repo_name):
        """
        Deletes the repository with name ``repo_name`` owned by the user with username ``username``.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository to delete
        :param str repo_name: name of repository to delete
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}".format(u=username, r=repo_name)
        self._check_ok(self._delete(path, auth=auth))

    def create_user(self, auth, login_name, username, email, password, send_notify=False):
        """
        Creates a new user, and returns the created user.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str login_name: login name for created user
        :param str username: username for created user
        :param str email: email address for created user
        :param str password: password for created user
        :param bool send_notify: whether a notification email should be sent upon creation
        :return: a representation of the created user
        :rtype: GogsUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        # Since the source_id parameter was not well-documented at the time this method was
        # written, force the default value
        data = {
            "login_name": login_name,
            "username": username,
            "email": email,
            "password": password,
            "send_notify": send_notify
        }
        response = self._post("/admin/users", auth=auth, data=data)
        self._check_ok(response)
        return GogsUser.from_json(response.json())

    def user_exists(self, username):
        """
        Returns whether a user with username ``username`` exists.

        :param str username: username of user
        :return: whether a user with the specified username exists
        :rtype: bool
        :raises NetworkFailure: if there is an error communicating with the server
        :return:
        """
        path = "/users/{}".format(username)
        return self._get(path).ok

    def search_users(self, username_keyword, limit=10):
        """
        Searches for users whose username matches ``username_keyword``, and returns
        a list of matched users.

        :param str username_keyword: keyword to search with
        :param int limit: maximum number of returned users
        :return: a list of matched users
        :rtype: List[GogsUser]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        params = {"q": username_keyword, "limit": limit}
        response = self._check_ok(self._get("/users/search", params=params))
        return [GogsUser.from_json(user_json) for user_json in response.json()["data"]]

    def get_user(self, auth, username):
        """
        Returns a representing the user with username ``username``.

        :param auth.Authentication auth: authentication object, can be ``None``
        :param str username: username of user to get
        :return: the retrieved user
        :rtype: GogsUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/users/{}".format(username)
        response = self._check_ok(self._get(path, auth=auth))
        return GogsUser.from_json(response.json())

    def update_user(self, auth, username, update):
        """
        Updates the user with username ``username`` according to ``update``.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str username: username of user to update
        :param GogsUserUpdate update: a ``GogsUserUpdate`` object describing the requested update
        :return: the updated user
        :rtype: GogsUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/admin/users/{}".format(username)
        response = self._check_ok(self._patch(path, auth=auth, data=update.as_dict()))
        return GogsUser.from_json(response.json())

    def delete_user(self, auth, username):
        """
        Deletes the user with username ``username``. Should only be called if the
        to-be-deleted user has no repositories.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str username: username of user to delete
        """
        path = "/admin/users/{}".format(username)
        self._check_ok(self._delete(path, auth=auth))

    # Helper methods

    def _delete(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.delete(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def _get(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.get(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def _patch(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.patch(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def _post(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.post(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    @staticmethod
    def _check_ok(response):
        """
        Raise exception if response is non-OK, otherwise return response
        """
        if not response.ok:
            GogsApi._fail(response)
        return response

    @staticmethod
    def _fail(response):
        """
        Raise an ApiFailure pertaining to the given response
        """
        message = "Status code: {}-{}, url: {}".format(response.status_code, response.reason, response.url)
        try:
            message += ", message:{}".format(response.json()[0]["message"])
        except Exception:
            pass
        raise ApiFailure(message, response.status_code)


class ApiFailure(Exception):
    """
    Raised to signal a failed request
    """
    def __init__(self, message, status_code):
        self._message = message
        self._status_code = status_code

    def __str__(self):
        return self._message

    @property
    def message(self):
        """
        An error message explaining why the request failed.

        :type: str
        """
        return self._message

    @property
    def status_code(self):
        """
        The HTTP status code of the response to the failed request

        :type: int
        """

        return self._status_code


class NetworkFailure(Exception):
    """
    Raised to signal a network-level failure
    """
    def __init__(self, cause=None):
        self._cause = cause

    def __str__(self):
        return "Caused by: {}".format(str(self._cause))

    @property
    def cause(self):
        """
        The exception causing the network failure

        :type: Exception
        """
        return self._cause
