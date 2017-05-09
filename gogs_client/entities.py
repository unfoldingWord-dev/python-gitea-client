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
    """
    Base class for an entity defined by the API

    """

    json = attr.ib()
    """
    :ivar json: Contains the json data
    :vartype: dict
    """

    @classmethod
    def from_json(cls, parsed_json):
        """
        Factory function to build an object based on JSON data
        """
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

    id = attr.ib()
    """
    The user's id (as *int*)
    """
    user_id = property(lambda self: self.id)
    """
    The user's id (as *int*) - *deprecated*
    """

    """
    The user's username (as *str*)
    """
    username = attr.ib()

    """
    The user's full name (as *str*)
    """
    full_name = attr.ib()

    """
    The user's email address. Can be empty as a result of invalid authentication (as *str*)
    """
    email = attr.ib(default=None)

    """
    The user's avatar URL (as *str*)
    """
    avatar_url = attr.ib(default=None)


@attr.s(frozen=True)
class GogsRepo(GogsEntity):
    """
    An immutable representation of a Gogs repository
    """

    id = attr.ib()
    """
    The repository's id (as *int*)
    """

    repo_id = property(lambda self: self.id)
    """
    The repository's id (as *int*) - *deprecated*
    """

    owner = attr.ib(convert=lambda parsed_json:GogsUser.from_json(parsed_json))
    """
    The owner of the repository (as *:obj:`GogsUser`*)
    """

    full_name = attr.ib()
    """
    The full name of the repository (as *str*)
    """

    private = attr.ib()
    """
    Whether the repository is private (as *bool*)
    """

    fork = attr.ib()
    """
    Whether the repository is a fork (as *bool*)
    """

    default_branch = attr.ib()
    """
    The name of the default branch (as *str*)
    """

    _ssh_url = attr.ib()
    _html_url = attr.ib()
    _clone_url = attr.ib()
    @property
    def urls(self):
        """
        URLs of the repository (as *:obj:`GogsRepo.Urls`*)
        """
        return GogsRepo.Urls(self._html_url, self._clone_url,self._ssh_url)

    permissions = attr.ib(convert=lambda data:GogsRepo.Permissions.from_json(data))
    """
    Permissions for the repository (as *:obj:`GogsRepo.Permissions`*)
    """

    parent = attr.ib(convert=lambda data:GogsRepo.from_json(data) if data else None, default=None)
    """
    Gets the repository's parent, when a fork (as *:obj:`GogsRepo`*)
    """

    empty = attr.ib(default=None)
    """
    Whether the repository is empty (as *bool*)
    """

    size = attr.ib(default=None)
    """
    Size of the repository in kilobytes (as *int*)
    """

    @attr.s(frozen=True)
    class Urls(object):
        """
        Class representating the possible URL for a resource
        """

        html_url = attr.ib()
        """
        URL for the repository's webpage (as *str*)
        """

        clone_url = attr.ib()
        """
        URL for cloning the repository (via HTTP) (as *str*)
        """

        ssh_url = attr.ib()
        """
        URL for cloning the repository via SSH (as *str*)
        """

    @attr.s(frozen=True)
    class Permissions(GogsEntity):
        """
        Class representating the permession of a resource
        """
        admin = attr.ib(default=False)
        """
        Whether the user that requested this repository has admin permissions (as *bool*)
        """

        push = attr.ib(default=False)
        """
        Whether the user that requested this repository has push permissions (as *bool*)
        """

        pull = attr.ib(default=False)
        """
        Whether the user that requested this repository has pull permissions (as *bool*)
        """

    @attr.s(frozen=True)
    class Hook(GogsEntity):
        id = attr.ib()
        """
        The hook's id number (as *int*)
        """
        hook_id = property(lambda self: self.id)
        """
        same as id (as *int*) - *deprecated*
        """

        type = attr.ib()
        """
        The hook's type (gogs, slack, etc.) (as *str*)
        """
        hook_type = property(lambda self: self.type)
        """
        same as type (as *str*) - *deprecated*
        """

        events = attr.ib()
        """
        The events that fire the hook (as *List[str]*)
        """

        active = attr.ib()
        """
        Whether the hook is active (as *bool*)
        """

        config = attr.ib()
        """
        Config of the hook. Possible keys include ``"content_type"``, ``"url"``, ``"secret"`` (as *dict*)
        """

    @attr.s(frozen=True)
    class DeployKey(GogsEntity):
        id = attr.ib()
        """
        The key's id number (as *int*)
        """
        key_id = property(lambda self: self.id)
        """
        The key's id number (as *int*)
        """

        key = attr.ib()
        """
        The content of the key (as *str*)
        """

        url = attr.ib()
        """
        URL where the key can be found (as *str*)
        """

        title = attr.ib()
        """
        The name of the key (as *str*)
        """

        created_at = attr.ib()
        """
        Creation date of the key (as *str*)
        """

        read_only = attr.ib()
        """
        Whether key is read-only (as *bool*)
        """


@attr.s(frozen=True)
class GogsOrg(GogsEntity):
    """
     An immutable representation of a Gogs Organization
    """

    id = attr.ib()
    """
    The organization's id (as *int*)
    """
    org_id = property(lambda self: self.id)
    """
    same as id (as *int*) - *deprecated*
    """

    username = attr.ib()
    """
    Organization's username (as *str*)
    """

    full_name = attr.ib()
    """
    Organization's full name (as *str*)
    """

    avatar_url = attr.ib()
    """
    Organization's avatar url (as *str*)
    """

    description = attr.ib()
    """
    Organization's description (as *str*)
    """

    website = attr.ib()
    """
    Organization's website address (as *str*)
    """

    location = attr.ib()
    """
    Organization's location (as *str*)
    """

@attr.s(frozen=True)
class GogsTeam(GogsEntity):
    """
    An immutable representation of a Gogs organization team
    """

    id = attr.ib()
    """
    Team's id (as *int*)
    """
    team_id = property(lambda self: self.id)
    """
    Same as id (as *int*) - *deprecated*
    """

    name = attr.ib()
    """
    Team name (as *str*)
    """

    description = attr.ib()
    """
    Description of the team (as *str*)
    """

    permission = attr.ib()
    """
    Team permission, can be read, write or admin, default is read (as *int*)
    """

