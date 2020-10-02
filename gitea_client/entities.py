"""
Various immutable classes that represent Gitea entities.
"""

from collections import OrderedDict

import attr


def json_get(parsed_json, key):
    """
    Retrieves the key from a parsed_json dictionary, or raises an exception if the
    key is not present
    """
    if key not in parsed_json:
        raise ValueError("JSON does not contain a {} field".format(key))
    return parsed_json[key]


@attr.s
class GiteaEntity(object):
    json = attr.ib()

    @classmethod
    def from_json(cls, parsed_json):
        # with introspection, get arguments of the constructor
        parsed_json['json'] = parsed_json.copy()
        params = cls.__attrs_attrs__
        args = []
        kwargs = OrderedDict()
        for param in params:
            param_name = param.name.lstrip('_')
            # if not a keyword argument
            if param.default == attr.NOTHING:
                args.append(json_get(parsed_json, param_name))
            # if it's a keyword argument
            else:
                kwargs[param_name] = parsed_json.get(param_name, None)
        o = cls(*args, **kwargs)
        return o


@attr.s(frozen=True)
class GiteaUser(GiteaEntity):
    """
     An immutable representation of a Gitea user
    """

    #: The user's id
    #:
    #: :type: int
    id = attr.ib()

    #: The user's id
    #:
    #: :type: int
    #:
    #: .. deprecated:: 1.1
    #:    Use :data:`id` instead
    user_id = property(lambda self: self.id)

    #: The user's username
    #:
    #: :type: str
    username = attr.ib()

    #: The user's full name
    #:
    #: :type: str
    full_name = attr.ib()

    #: The user's email address. Can be empty as a result of invalid authentication
    #:
    #: :type: str
    email = attr.ib(default=None)

    #: The user's avatar URL
    #:
    #: :type: str
    avatar_url = attr.ib(default=None)


@attr.s(frozen=True)
class GiteaRepo(GiteaEntity):
    """
    An immutable representation of a Gitea repository
    """

    #: The repository's id
    #:
    #: :type: int
    id = attr.ib()

    #: The repository's id
    #:
    #: :type: int
    #:
    #: .. deprecated:: 1.1
    #:    Use :data:`id` instead
    repo_id = property(lambda self: self.id)

    #: The owner of the repository
    #:
    #: :type: :class:`~GiteaUser`
    owner = attr.ib(converter=lambda parsed_json: GiteaUser.from_json(parsed_json))

    #: The name of the repository
    #:
    #: :type: str
    name = attr.ib()

    #: The full name of the repository
    #:
    #: :type: str
    full_name = attr.ib()

    #: Whether the repository is private
    #:
    #: :type: bool
    private = attr.ib()

    #: Whether the repository is a fork
    #:
    #: :type: bool
    fork = attr.ib()

    #: The name of the default branch
    #:
    #: :type: str
    default_branch = attr.ib()

    _html_url = attr.ib()
    _ssh_url = attr.ib()
    _clone_url = attr.ib()

    @property
    def urls(self):
        """
        URLs of the repository

        :type: :class:`~GiteaRepo.Urls`
        """
        return GiteaRepo.Urls(self._html_url, self._clone_url, self._ssh_url)

    #: Permissions for the repository
    #:
    #: :type: :class:`~GiteaRepo.Permissions`
    permissions = attr.ib(converter=lambda data: GiteaRepo.Permissions.from_json(data))

    #: Gets the repository's parent, when a fork
    #:
    #: :type: :class:`~GiteaRepo`
    parent = attr.ib(converter=lambda data: GiteaRepo.from_json(data) if data else None, default=None)

    #: The description of the repository
    #:
    #: :type: str
    description = attr.ib(default=None)

    #: Whether the repository is empty
    #:
    #: :type: bool
    empty = attr.ib(default=None)

    #: Size of the repository in kilobytes
    #:
    #: :type: int
    size = attr.ib(default=None)

    @attr.s(frozen=True)
    class Urls(object):
        #: URL for the repository's webpage
        #:
        #: :type: str
        html_url = attr.ib()

        #: URL for cloning the repository (via HTTP)
        #:
        #: :type: str
        clone_url = attr.ib()

        #: URL for cloning the repository via SSH
        #:
        #: :type: str
        ssh_url = attr.ib()

    @attr.s(frozen=True)
    class Permissions(GiteaEntity):
        #: Whether the user that requested this repository has admin permissions
        #:
        #: :type: bool
        admin = attr.ib(default=False)

        #: Whether the user that requested this repository has push permissions
        #:
        #: :type: bool
        push = attr.ib(default=False)

        #: Whether the user that requested this repository has pull permissions
        #:
        #: :type: bool
        pull = attr.ib(default=False)

    @attr.s(frozen=True)
    class Hook(GiteaEntity):
        #: The hook's id number
        #:
        #: :type: int
        id = attr.ib()

        #: The hook's id number
        #:
        #: :type: int
        #:
        #: .. deprecated:: 1.1
        #:    Use :data:`id` instead
        hook_id = property(lambda self: self.id)

        #: The hook's type (gitea, slack, etc.)
        #:
        #: :type: str
        type = attr.ib()

        #: The hook's type (gitea, slack, etc.)
        #:
        #: :type: str
        #:
        #: .. deprecated:: 1.1
        #:    Use :data:`type` instead
        hook_type = property(lambda self: self.type)

        #: The events that fire the hook
        #:
        #: :type: List[str]
        events = attr.ib()

        #: Whether the hook is active
        #:
        #: :type: bool
        active = attr.ib()

        #: Config of the hook. Possible keys include ``"content_type"``, ``"url"``, ``"secret"``
        #:
        #: :type: dict
        config = attr.ib()

    @attr.s(frozen=True)
    class DeployKey(GiteaEntity):
        #: The key's id number
        #:
        #: :type: int
        id = attr.ib()

        #: The key's id number
        #:
        #: :type: int
        #:
        #: .. deprecated:: 1.1
        #:    Use :data:`id` instead
        key_id = property(lambda self: self.id)

        #: The content of the key
        #:
        #: :type: str
        key = attr.ib()

        #: URL where the key can be found
        #:
        #: :type: str
        url = attr.ib()

        #: The name of the key
        #:
        #: :type: str
        title = attr.ib()

        #: Creation date of the key
        #:
        #: :type: str
        created_at = attr.ib()

        #: Whether key is read-only
        #:
        #: :type: bool
        read_only = attr.ib()


@attr.s(frozen=True)
class GiteaBranch(GiteaEntity):
    """
    An immutable representation of a Gitea branch
    """

    #: The branch's name
    #:
    #: :type: str
    name = attr.ib()

    #: The HEAD commit of the branch
    #:
    #: :type: :class:`~GiteaCommit`
    commit = attr.ib(converter=lambda parsed_json: GiteaCommit.from_json(parsed_json))


@attr.s(frozen=True)
class GiteaCommit(GiteaEntity):
    """
    An immutable representation of a Gitea commit
    """

    #: The commit's id
    #:
    #: :type: str
    id = attr.ib()

    #: The commit's message
    #:
    #: :type: str
    message = attr.ib()

    #: The commit's url
    #:
    #: :type: str
    url = attr.ib()

    #: The commit's timestamp
    #:
    #: :type: str
    timestamp = attr.ib()


@attr.s(frozen=True)
class GiteaOrg(GiteaEntity):
    """
     An immutable representation of a Gitea organization
    """

    #: The organization's id
    #:
    #: :type: int
    id = attr.ib()

    #: The organization's id
    #:
    #: :type: int
    #:
    #: .. deprecated:: 1.1
    #:    Use :data:`id` instead
    org_id = property(lambda self: self.id)

    #: Organization's username
    #:
    #: :type: str
    username = attr.ib()

    #: Organization's full name
    #:
    #: :type: str
    full_name = attr.ib()

    #: Organization's avatar URL
    #:
    #: :type: str
    avatar_url = attr.ib()

    #: Organization's description
    #:
    #: :type: str
    description = attr.ib()

    #: Organization's website address
    #:
    #: :type: str
    website = attr.ib()

    #: Organization's location
    #:
    #: :type: str
    location = attr.ib()


@attr.s(frozen=True)
class GiteaTeam(GiteaEntity):
    """
    An immutable representation of a Gitea organization team
    """

    #: Team's id
    #:
    #: :type: int
    id = attr.ib()

    #: Team's id
    #:
    #: :type: int
    #:
    #: .. deprecated:: 1.1
    #:    Use :data:`id` instead
    team_id = property(lambda self: self.id)

    #: Team name
    #:
    #: :type: str
    name = attr.ib()

    #: Description of the team
    #:
    #: :type: str
    description = attr.ib()

    #: Team permission, one of `"read"`, `"write"`, `"admin"`, `"owner"` or `"none"`
    #:
    #: :type: str
    permission = attr.ib()
