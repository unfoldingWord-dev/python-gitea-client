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


class GogsEntity(object):
    def __init__(self, json):
        self._json = json

    @property
    def json(self):
        return self._json

class GogsUser(GogsEntity):
    """
     An immutable representation of a Gogs user
    """

    def __init__(self, user_id, username, full_name, email, avatar_url, json={}):
        super(GogsUser, self).__init__(json=json)
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
                        email=email, avatar_url=avatar_url, json=parsed_json)

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


class GogsRepo(GogsEntity):
    """
    An immutable representation of a Gogs repository
    """

    def __init__(self, repo_id, owner, full_name, private, fork, parent_id, default_branch,
            empty, size, urls, permissions, json={}):
        super(GogsRepo, self).__init__(json=json)
        self._repo_id = repo_id
        self._owner = owner
        self._full_name = full_name
        self._private = private
        self._fork = fork
        self._parent_id = parent_id
        self._default_branch = default_branch
        self._empty = empty
        self._size = size
        self._urls = urls
        self._permissions = permissions

    @staticmethod
    def from_json(parsed_json):
        repo_id = json_get(parsed_json, "id")
        owner = GogsUser.from_json(json_get(parsed_json, "owner"))
        full_name = json_get(parsed_json, "full_name")
        private = json_get(parsed_json, "private")
        fork = json_get(parsed_json, "fork")
        parent_id = parsed_json.get("parent_id", None)
        default_branch = json_get(parsed_json, "default_branch")
        empty = parsed_json.get("empty", None)
        size = parsed_json.get("size", None)
        urls = GogsRepo.Urls(json_get(parsed_json, "html_url"), json_get(parsed_json, "clone_url"),
                             json_get(parsed_json, "ssh_url"))
        permissions = GogsRepo.Permissions.from_json(json_get(parsed_json, "permissions"))
        return GogsRepo(repo_id=repo_id, owner=owner, full_name=full_name, private=private, fork=fork,
                        parent_id=parent_id, default_branch=default_branch, empty=empty, size=size,
                        urls=urls, permissions=permissions, json=parsed_json)

    @property  # named repo_id to avoid conflict with built-in id
    def repo_id(self):
        """
        The repository's id

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
    def parent_id(self):
        """
        Gets the repository's parent, when a fork

        :rtype: int
        """
        return self.parent_id

    @property
    def default_branch(self):
        """
        The name of the default branch

        :rtype: str
        """
        return self._default_branch

    @property
    def empty(self):
        """
        Whether the repository is empty

        :rtype: bool
        """
        return self._empty

    @property
    def size(self):
        """
        Size of the repository in kilobytes

        :rtype: int
        """
        return self._size

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

            :rtype: str
            """
            return self._ssh_url

    class Permissions(GogsEntity):
        def __init__(self, admin, push, pull, json={}):
            super(GogsRepo.Permissions, self).__init__(json=json)
            self._admin = admin
            self._push = push
            self._pull = pull

        @staticmethod
        def from_json(parsed_json):
            admin = parsed_json.get("admin", False)
            push = parsed_json.get("push", False)
            pull = parsed_json.get("pull", False)
            return GogsRepo.Permissions(admin, push, pull, parsed_json)

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

    class Hook(GogsEntity):
        def __init__(self, hook_id, hook_type, events, active, config, json={}):
            super(GogsRepo.Hook, self).__init__(json=json)
            self._id = hook_id
            self._type = hook_type
            self._events = events
            self._active = active
            self._config = config

        @staticmethod
        def from_json(parsed_json):
            hook_id = json_get(parsed_json, "id")
            hook_type = json_get(parsed_json, "type")
            events = json_get(parsed_json, "events")
            active = json_get(parsed_json, "active")
            config = json_get(parsed_json, "config")
            return GogsRepo.Hook(hook_id=hook_id, hook_type=hook_type, events=events, active=active,
                                 config=config, json=parsed_json)

        @property  # named hook_id to avoid conflict with built-in id
        def hook_id(self):
            """
            The hook's id number

            :rtype: int
            """
            return self._id

        @property  # named hook_type to avoid conflict with built-in type
        def hook_type(self):
            """
            The hook's type (gogs, slack, etc.)

            :rtype: str
            """
            return self._type

        @property
        def events(self):
            """
            The events that fire the hook

            :rtype: List[str]
            """
            return self._events

        @property
        def active(self):
            """
            Whether the hook is active

            :rtype: bool
            """
            return self._active

        @property
        def config(self):
            """
            Config of the hook. Possible keys include ``"content_type"``, ``"url"``, ``"secret"``

            :rtype: dict
            """
            return self._config

    class DeployKey(GogsEntity):
        def __init__(self, key_id, key, url, title, created_at, read_only, json={}):
            super(GogsRepo.DeployKey, self).__init__(json=json)
            self._id = key_id
            self._key = key
            self._url = url
            self._title = title
            self._created_at = created_at
            self._read_only = read_only

        @staticmethod
        def from_json(parsed_json):
            key_id = json_get(parsed_json, "id")
            key = json_get(parsed_json, "key")
            url = json_get(parsed_json, "url")
            title = json_get(parsed_json, "title")
            created_at = json_get(parsed_json, "created_at")
            read_only = json_get(parsed_json, "read_only")

            return GogsRepo.DeployKey(key_id=key_id, key=key, url=url,
                                      title=title, created_at=created_at,
                                      read_only=read_only, json=parsed_json)

        @property  # named key_id to avoid conflict with built-in id
        def key_id(self):
            """
            The key's id number

            :rtype: int
            """
            return self._id

        @property
        def key(self):
            """
            The content of the key

            :rtype: str
            """
            return self._key

        @property
        def url(self):
            """
            URL where the key can be found

            :rtype: str
            """
            return self._url

        @property
        def title(self):
            """
            The name of the key

            :rtype: str
            """
            return self._title

        @property
        def created_at(self):
            """
            Creation date of the key

            :rtype: str
            """
            return self._created_at

        @property
        def read_only(self):
            """
            Whether key is read-only

            :rtype: bool
            """
            return self._read_only


class GogsOrg(GogsEntity):
    """
     An immutable representation of a Gogs Organization
    """

    def __init__(self, org_id, username, full_name, avatar_url, description, website, location, json={}):
        super(GogsOrg, self).__init__(json=json)
        self._id = org_id
        self._username = username
        self._full_name = full_name
        self._avatar_url = avatar_url
        self._description = description
        self._website = website
        self._location = location

    @staticmethod
    def from_json(parsed_json):
        org_id = json_get(parsed_json, "id")
        username = json_get(parsed_json, "username")
        full_name = json_get(parsed_json, "full_name")
        avatar_url = json_get(parsed_json, "avatar_url")
        description = json_get(parsed_json, "description")
        website = json_get(parsed_json, "website")
        location = json_get(parsed_json, "location")
        return GogsOrg(org_id=org_id, username=username, full_name=full_name,
                       avatar_url=avatar_url, description=description,
                       website=website, location=location, json=parsed_json)

    @property  # named org_id to avoid conflict with built-in id
    def org_id(self):
        """
        The organization's id

        :rtype: int
        """
        return self._id

    @property
    def username(self):
        """
        Organization's username

        :rtype: str
        """
        return self._username

    @property
    def full_name(self):
        """
        Organization's full name

        :rtype: str
        """
        return self._full_name

    @property
    def avatar_url(self):
        """
        Organization's avatar url

        :rtype: str
        """
        return self._avatar_url

    @property
    def description(self):
        """
        Organization's description

        :rtype: str
        """
        return self._description

    @property
    def website(self):
        """
        Organization's website address

        :rtype: str
        """
        return self._website

    @property
    def location(self):
        """
        Organization's location

        :rtype: str
        """
        return self._location


class GogsTeam(GogsEntity):
    """
    An immutable representation of a Gogs organization team
    """
    def __init__(self, team_id, name, description, permission, json={}):
        super(GogsTeam, self).__init__(json=json)
        self._id = team_id
        self._name = name
        self._description = description
        self._permission = permission

    @staticmethod
    def from_json(parsed_json):
        team_id = json_get(parsed_json, "id")
        name = json_get(parsed_json, "name")
        description = json_get(parsed_json, "description")
        permission = json_get(parsed_json, "permission")
        return GogsTeam(team_id=team_id, name=name, description=description,
                permission=permission, json=parsed_json)

    @property  # named team_id to avoid conflict with built-in id
    def team_id(self):
        """
        Team's id

        :rtype: int
        """
        return self._id

    @property
    def name(self):
        """
        Team name

        :rtype: str
        """
        return self._name

    @property
    def description(self):
        """
        Description of the team

        :rtype: str
        """
        return self._description

    @property
    def permission(self):
        """
        Team permission, can be read, write or admin, default is read

        :rtype: int
        """
        return self._permission
