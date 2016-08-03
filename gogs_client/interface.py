import requests

from gogs_client.entities import GogsUser, GogsRepo
from gogs_client.http_utils import RelativeHttpRequestor, append_url


class GogsApi(object):
    """
    A Gogs client, serving as a wrapper around the Gogs HTTP API.

    All public-facing methods can raise two types of Exceptions:
    1. GogsApi.NetworkFailure: raised if the Gogs server cannot be reached due to a
         network-level error.
    2. GogsApi.ApiFailure: raised if a request expecting a successful response does not get
         a successful response. For example, looking up a repository that does not exist or
         authenticating with an invalid token will result in a GogsApi.ApiFailure being
         raised
    """

    def __init__(self, base_url):
        """
        :param base_url: Root API endpoint. Should be given with HTTPS protocol
        """
        api_base = append_url(base_url, "/api/v1/")
        self._requestor = RelativeHttpRequestor(api_base)

    def valid_authentication(self, auth):
        """
        :type auth: GogsAuthentication - authenticate to check/validate
        :return: whether the provided token is a valid user token
        """
        return self._get("/user/repos", auth=auth).ok

    def create_repo(self, auth, name, description=None, private=False, auto_init=False,
                    gitignore_templates=None, license_template=None, readme_template=None):
        """
        :param auth: GogsAuthentication
        :param name: name for repo
        :param description:
        :param private:
        :param auto_init: if the created repo should be auto-initialized with an intial commit
        :param gitignore_templates: collection of gitignore templates to apply
        :param license_template: license template to apply
        :param readme_template: README template to apply
        :return: GogsRepo representing created repository
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
        path = "/repos/{u}/{r}".format(u=username, r=repo_name)
        return self._get(path, auth=auth).ok

    def get_repo(self, auth, username, repo_name):
        """
        :return: GogsRepo of corresponding repository
        """
        path = "/repos/{u}/{r}".format(u=username, r=repo_name)
        response = self._check_ok(self._get(path, auth=auth))
        return GogsRepo.from_json(response.json())

    def delete_repo(self, auth, owner_username, repo_name):
        path = "/repos/{o}/{r}".format(o=owner_username, r=repo_name)
        self._check_ok(self._delete(path, auth=auth))

    def create_user(self, auth, login_name, username, email, password, send_notify=False):
        """
        :param auth: GogsAuthentication, should be admin
        :param login_name:
        :param username:
        :param email:
        :param password:
        :param send_notify: If a notification email should be sent. Only should be True if a
            mailing service has been set up
        :return: GogsUser representing created user
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
        path = "/users/{}".format(username)
        return self._get(path).ok

    def search_users(self, username_keyword, limit=10):
        """
        :return: list of found users (i.e. GogsUser objects)
        """
        params = {"q": username_keyword, "limit": limit}
        response = self._check_ok(self._get("/users/search", params=params))
        return [GogsUser.from_json(user_json) for user_json in response.json()["data"]]

    def get_user(self, auth, username):
        """
        :return: GogsUser of user with username
        """
        path = "/users/{}".format(username)
        response = self._check_ok(self._get(path, auth=auth))
        return GogsUser.from_json(response.json())

    def update_user(self, auth, username, update):
        """
        :param auth: GogsAuthentication
        :param username: username of user to update
        :param update: GogsUserUpdate representing the requested update
        :return: GogsUser representing updated user
        """
        path = "/admin/users/{}".format(username)
        response = self._check_ok(self._patch(path, auth=auth, data=update.as_dict()))
        return GogsUser.from_json(response.json())

    def delete_user(self, auth, username):
        """
        Should only be called if the about-to-be-deleted user has no repositories
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
            raise GogsApi.NetworkFailure(exc)

    def _get(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.get(path, **kwargs)
        except requests.RequestException as exc:
            raise GogsApi.NetworkFailure(exc)

    def _patch(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.patch(path, **kwargs)
        except requests.RequestException as exc:
            raise GogsApi.NetworkFailure(exc)

    def _post(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.post(path, **kwargs)
        except requests.RequestException as exc:
            raise GogsApi.NetworkFailure(exc)

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
        raise GogsApi.ApiFailure(message, response.status_code)

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
        def message(self): return self._message

        @property
        def status_code(self): return self._status_code

    class NetworkFailure(Exception):
        """
        Raised to signal a network failure
        """
        def __init__(self, cause=None):
            self._cause = cause

        def __str__(self):
            return "Caused by: {}".format(str(self._cause))

        @property
        def cause(self): return self._cause
