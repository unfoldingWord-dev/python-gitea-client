"""
Various immutable classes that represent Gogs entities.
"""


def json_get(parsed_json, key):
    """
    Retrieves the key from a parsed_json dictionary, or raises an exception if the
    key is not present
    """
    if key not in parsed_json:
        raise ValueError("JSON does not contain a {} field".format(key))
    return parsed_json[key]


class GogsUser(object):
    """
     An immutable representation of a Gogs user.
    """
    def __init__(self, user_id, username, full_name, email, avatar_url):
        self._id = user_id
        self._username = username
        self._full_name = full_name
        self._email = email
        self._avatar_url = avatar_url

    @staticmethod
    def from_json(parsed_json):
        user_id = json_get(parsed_json, "id")
        username = json_get(parsed_json, "username")
        full_name = json_get(parsed_json, "full_name")
        email = parsed_json.get("email", None)
        avatar_url = parsed_json.get("avatar_url", None)
        return GogsUser(user_id=user_id, username=username, full_name=full_name,
                        email=email, avatar_url=avatar_url)

    @property  # named user_id to avoid conflict with built-in id
    def user_id(self):
        """
        The user's id

        :rtype: int
        """
        return self._id

    @property
    def username(self):
        """
        The user's username

        :rtype: str
        """
        return self._username

    @property
    def full_name(self):
        """
        The user's full name

        :rtype: str
        """
        return self._full_name

    @property
    def email(self):
        """
        The user's email address. Can be empty as a result of invalid authentication

        :rtype: str
        """
        return self._email

    @property
    def avatar_url(self):
        """
        The user's avatar URL

        :rtype: str
        """
        return self._avatar_url


class GogsRepo(object):
    """
    An immutable representation of a Gogs repository
    """

    def __init__(self, repo_id, owner, full_name, private, fork, urls, permissions):
        self._repo_id = repo_id
        self._owner = owner
        self._full_name = full_name
        self._private = private
        self._fork = fork
        self._urls = urls
        self._permissions = permissions

    @staticmethod
    def from_json(parsed_json):
        repo_id = json_get(parsed_json, "id")
        owner = GogsUser.from_json(json_get(parsed_json, "owner"))
        full_name = json_get(parsed_json, "full_name")
        private = json_get(parsed_json, "private")
        fork = json_get(parsed_json, "fork")
        urls = GogsRepo.Urls(json_get(parsed_json, "html_url"), json_get(parsed_json, "clone_url"),
                             json_get(parsed_json, "ssh_url"))
        permissions = GogsRepo.Permissions.from_json(json_get(parsed_json, "permissions"))
        return GogsRepo(repo_id=repo_id, owner=owner, full_name=full_name, private=private, fork=fork,
                        urls=urls, permissions=permissions)

    @property  # named repo_id to avoid conflict with built-in id
    def repo_id(self):
        """
        The repository's id number

        :rtype: int
        """
        return self._repo_id

    @property
    def owner(self):
        """
        The owner of the repository

        :rtype: entities.GogsUser
        """
        return self._owner

    @property
    def full_name(self):
        """
        The full name of the repository

        :rtype: str
        """
        return self._full_name

    @property
    def private(self):
        """
        Whether the repository is private

        :rtype: bool
        """
        return self._private

    @property
    def fork(self):
        """
        Whether the repository is a fork

        :rtype: bool
        """
        return self._fork

    @property
    def urls(self):
        """
        URLs of the repository

        :rtype: GogsRepo.Urls
        """
        return self._urls

    @property
    def permissions(self):
        """
        Permissions for the repository

        :rtype: GogsRepo.Permissions
        """
        return self._permissions

    class Urls(object):
        def __init__(self, html_url, clone_url, ssh_url):
            self._html_url = html_url
            self._clone_url = clone_url
            self._ssh_url = ssh_url

        @property
        def html_url(self):
            """
            URL for the repository's webpage
            :rtype: str
            """
            return self._html_url

        @property
        def clone_url(self):
            """
            URL for cloning the repository (via HTTP)

            :rtype: str
            """
            return self._clone_url

        @property
        def ssh_url(self):
            """
            URL for cloning the repository via SSH
            :rtype:
            """
            return self._ssh_url

    class Permissions(object):
        def __init__(self, admin, push, pull):
            self._admin = admin
            self._push = push
            self._pull = pull

        @staticmethod
        def from_json(parsed_json):
            admin = parsed_json.get("admin", False)
            push = parsed_json.get("push", False)
            pull = parsed_json.get("pull", False)
            return GogsRepo.Permissions(admin, push, pull)

        @property
        def admin(self):
            """
            Whether the user that requested this repository has admin permissions

            :rtype: bool
            """
            return self._admin

        @property
        def push(self):
            """
            Whether the user that requested this repository has push permissions

            :rtype: bool
            """
            return self._push

        @property
        def pull(self):
            """
            Whether the user that requested this repository has pull permissions

            :rtype: bool
            """
            return self._pull
