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

import attr

from collections import OrderedDict

@attr.s
class GogsEntity(object):
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
class GogsUser(GogsEntity):
    """
     An immutable representation of a Gogs user
    """

    """
    The user's id

    :rtype: int
    """
    id = attr.ib()
    user_id = property(lambda self: self.id)

    """
    The user's username

    :rtype: str
    """
    username = attr.ib()

    """
    The user's full name

    :rtype: str
    """
    full_name = attr.ib()

    """
    The user's email address. Can be empty as a result of invalid authentication

    :rtype: str
    """
    email = attr.ib(default=None)

    """
    The user's avatar URL

    :rtype: str
    """
    avatar_url = attr.ib(default=None)


@attr.s(frozen=True)
class GogsRepo(GogsEntity):
    """
    An immutable representation of a Gogs repository
    """

    """
    The repository's id

    :rtype: int
    """
    id = attr.ib()
    repo_id = property(lambda self: self.id)

    """
    The owner of the repository

    :rtype: entities.GogsUser
    """
    owner = attr.ib(convert=lambda parsed_json:GogsUser.from_json(parsed_json))

    """
    The full name of the repository

    :rtype: str
    """
    full_name = attr.ib()

    """
    Whether the repository is private

    :rtype: bool
    """
    private = attr.ib()

    """
    Whether the repository is a fork

    :rtype: bool
    """
    fork = attr.ib()

    """
    The name of the default branch

    :rtype: str
    """
    default_branch = attr.ib()

    """
    URLs of the repository

    :rtype: GogsRepo.Urls
    """
    _ssh_url = attr.ib()
    _html_url = attr.ib()
    _clone_url = attr.ib()
    @property
    def urls(self):
        return GogsRepo.Urls(self._html_url, self._clone_url,self._ssh_url)

    """
    Permissions for the repository

    :rtype: GogsRepo.Permissions
    """
    permissions = attr.ib(convert=lambda data:GogsRepo.Permissions.from_json(data))

    """
    Gets the repository's parent, when a fork

    :rtype: GogsRepo
    """
    parent = attr.ib(convert=lambda data:GogsRepo.from_json(data) if data else None, default=None)

    """
    Whether the repository is empty

    :rtype: bool
    """
    empty = attr.ib(default=None)

    """
    Size of the repository in kilobytes

    :rtype: int
    """
    size = attr.ib(default=None)

    @attr.s(frozen=True)
    class Urls(object):
        """
        URL for the repository's webpage

        :rtype: str
        """
        html_url = attr.ib()

        """
        URL for cloning the repository (via HTTP)

        :rtype: str
        """
        clone_url = attr.ib()

        """
        URL for cloning the repository via SSH

        :rtype: str
        """
        ssh_url = attr.ib()

    @attr.s(frozen=True)
    class Permissions(GogsEntity):
        """
        Whether the user that requested this repository has admin permissions

        :rtype: bool
        """
        admin = attr.ib(default=False)

        """
        Whether the user that requested this repository has push permissions

        :rtype: bool
        """
        push = attr.ib(default=False)

        """
        Whether the user that requested this repository has pull permissions

        :rtype: bool
        """
        pull = attr.ib(default=False)

    @attr.s(frozen=True)
    class Hook(GogsEntity):
        """
        The hook's id number

        :rtype: int
        """
        id = attr.ib()
        hook_id = property(lambda self: self.id)

        """
        The hook's type (gogs, slack, etc.)

        :rtype: str
        """
        type = attr.ib()
        hook_type = property(lambda self: self.type)

        """
        The events that fire the hook

        :rtype: List[str]
        """
        events = attr.ib()

        """
        Whether the hook is active

        :rtype: bool
        """
        active = attr.ib()

        """
        Config of the hook. Possible keys include ``"content_type"``, ``"url"``, ``"secret"``

        :rtype: dict
        """
        config = attr.ib()

    @attr.s(frozen=True)
    class DeployKey(GogsEntity):
        """
        The key's id number

        :rtype: int
        """
        id = attr.ib()
        key_id = property(lambda self: self.id)

        """
        The content of the key

        :rtype: str
        """
        key = attr.ib()

        """
        URL where the key can be found

        :rtype: str
        """
        url = attr.ib()

        """
        The name of the key

        :rtype: str
        """
        title = attr.ib()

        """
        Creation date of the key

        :rtype: str
        """
        created_at = attr.ib()

        """
        Whether key is read-only

        :rtype: bool
        """
        read_only = attr.ib()


@attr.s(frozen=True)
class GogsOrg(GogsEntity):
    """
     An immutable representation of a Gogs Organization
    """

    """
    The organization's id

    :rtype: int
    """
    id = attr.ib()
    org_id = property(lambda self: self.id)

    """
    Organization's username

    :rtype: str
    """
    username = attr.ib()

    """
    Organization's full name

    :rtype: str
    """
    full_name = attr.ib()

    """
    Organization's avatar url

    :rtype: str
    """
    avatar_url = attr.ib()

    """
    Organization's description

    :rtype: str
    """
    description = attr.ib()

    """
    Organization's website address

    :rtype: str
    """
    website = attr.ib()

    """
    Organization's location

    :rtype: str
    """
    location = attr.ib()

@attr.s(frozen=True)
class GogsTeam(GogsEntity):
    """
    An immutable representation of a Gogs organization team
    """

    """
    Team's id

    :rtype: int
    """
    id = attr.ib()
    team_id = property(lambda self: self.id)

    """
    Team name

    :rtype: str
    """
    name = attr.ib()

    """
    Description of the team

    :rtype: str
    """
    description = attr.ib()

    """
    Team permission, can be read, write or admin, default is read

    :rtype: int
    """
    permission = attr.ib()

