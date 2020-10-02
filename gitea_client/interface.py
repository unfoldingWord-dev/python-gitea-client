import requests

from gitea_client._implementation.http_utils import RelativeHttpRequestor, append_url
from gitea_client.auth import Token
from gitea_client.entities import GiteaUser, GiteaRepo, GiteaBranch, GiteaOrg, GiteaTeam


class GiteaApi(object):
    """
    A Gitea client, serving as a wrapper around the Gitea HTTP API.
    """

    def __init__(self, base_url, session=None):
        """
        :param str base_url: the URL of the Gitea server to communicate with. Should be given
                             with the https protocol
        :param requests.Session session: a ``requests`` session instance
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
        :rtype: GiteaUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        response = self.get("/user", auth=auth)
        return GiteaUser.from_json(response.json())

    def get_tokens(self, auth, username=None):
        """
        Returns the tokens owned by the specified user. If no user is specified,
        uses the user authenticated by ``auth``.

        :param auth.Authentication auth: authentication for user to retrieve.
                                         Must be a username-password authentication,
                                         due to a restriction of the Gitea API
        :param str username: username of owner of tokens

        :return: list of tokens
        :rtype: List[Token]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        if username is None:
            username = self.authenticated_user(auth).username
        response = self.get("/users/{u}/tokens".format(u=username), auth=auth)
        return [Token.from_json(o) for o in response.json()]

    def create_token(self, auth, name, username=None):
        """
        Creates a new token with the specified name for the specified user.
        If no user is specified, uses user authenticated by ``auth``.

        :param auth.Authentication auth: authentication for user to retrieve.
                                         Must be a username-password authentication,
                                         due to a restriction of the Gitea API
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
        response = self.post("/users/{u}/tokens".format(u=username), auth=auth, data=data)
        return Token.from_json(response.json())

    def ensure_token(self, auth, name, username=None):
        """
        Ensures the existence of a token with the specified name for the
        specified user. Creates a new token if none exists. If no user is
        specified, uses user authenticated by ``auth``.

        :param auth.Authentication auth: authentication for user to retrieve.
                                         Must be a username-password authentication,
                                         due to a restriction of the Gitea API
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
        if len(tokens) > 0:
            return tokens[0]
        return self.create_token(auth, name, username)

    def create_repo(self, auth, name, description=None, private=False, auto_init=False,
                    gitignore_templates=None, license_template=None, readme_template=None,
                    organization=None):
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
        :param str organization: organization under which repository is created
        :return: a representation of the created repository
        :rtype: GiteaRepo
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
        url = "/org/{0}/repos".format(organization) if organization else "/user/repos"
        response = self.post(url, auth=auth, data=data)
        return GiteaRepo.from_json(response.json())

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
        :rtype: GiteaRepo
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}".format(u=username, r=repo_name)
        response = self.get(path, auth=auth)
        return GiteaRepo.from_json(response.json())

    def get_user_repos(self, auth, username):
        """
        Returns the repositories  owned by
        the user with username ``username``.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :return: a list of repositories
        :rtype: List[GiteaRepo]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/users/{u}/repos".format(u=username)
        response = self.get(path, auth=auth)
        return [GiteaRepo.from_json(repo_json) for repo_json in response.json()]

    def get_branch(self, auth, username, repo_name, branch_name):
        """
        Returns the branch with name ``branch_name`` in the repository with name ``repo_name``
        owned by the user with username ``username``.

        :param auth.Authentication auth: authentication object 
        :param str username: username of owner of repository containing the branch
        :param str repo_name: name of the repository with the branch
        :param str branch_name: name of the branch to return
        :return: a branch
        :rtype: GiteaBranch
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}/branches/{b}".format(u=username, r=repo_name, b=branch_name)
        response = self.get(path, auth=auth)
        return GiteaBranch.from_json(response.json())

    def get_branches(self, auth, username, repo_name):
        """
        Returns the branches in the repository with name ``repo_name`` owned by the user
        with username ``username``.

        :param auth.Authentication auth: authentication object 
        :param str username: username of owner of repository containing the branch
        :param str repo_name: name of the repository with the branch
        :return: a list of branches
        :rtype: List[GiteaBranch]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}/branches".format(u=username, r=repo_name)
        response = self.get(path, auth=auth)
        return [GiteaBranch.from_json(branch_json) for branch_json in response.json()]

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
        self.delete(path, auth=auth)

    def migrate_repo(self, auth, clone_addr,
                     uid, repo_name, auth_username=None, auth_password=None,
                     mirror=False, private=False, description=None):
        """
        Migrate a repository from another Git hosting source for the authenticated user.

        :param auth.Authentication auth: authentication object
        :param str clone_addr: Remote Git address (HTTP/HTTPS URL or local path)
        :param int uid: user ID of repository owner
        :param str repo_name: Repository name
        :param bool mirror: Repository will be a mirror. Default is false
        :param bool private: Repository will be private. Default is false
        :param str description: Repository description
        :return: a representation of the migrated repository
        :rtype: GiteaRepo
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        # "auth_username": auth_username,
        # "auth_password": auth_password,

        data = {
            "clone_addr": clone_addr,
            "uid": uid,
            "repo_name": repo_name,
            "mirror": mirror,
            "private": private,
            "description": description,
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        url = "/repos/migrate"
        response = self.post(url, auth=auth, data=data)
        return GiteaRepo.from_json(response.json())

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
        :rtype: GiteaUser
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
        response = self.post("/admin/users", auth=auth, data=data)
        return GiteaUser.from_json(response.json())

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
        :rtype: List[GiteaUser]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        params = {"q": username_keyword, "limit": limit}
        response = self.get("/users/search", params=params)
        return [GiteaUser.from_json(user_json) for user_json in response.json()["data"]]

    def get_user(self, auth, username):
        """
        Returns a representing the user with username ``username``.

        :param auth.Authentication auth: authentication object, can be ``None``
        :param str username: username of user to get
        :return: the retrieved user
        :rtype: GiteaUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/users/{}".format(username)
        response = self.get(path, auth=auth)
        return GiteaUser.from_json(response.json())

    def update_user(self, auth, username, update):
        """
        Updates the user with username ``username`` according to ``update``.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str username: username of user to update
        :param GiteaUserUpdate update: a ``GiteaUserUpdate`` object describing the requested update
        :return: the updated user
        :rtype: GiteaUser
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/admin/users/{}".format(username)
        response = self.patch(path, auth=auth, data=update.as_dict())
        return GiteaUser.from_json(response.json())

    def delete_user(self, auth, username):
        """
        Deletes the user with username ``username``. Should only be called if the
        to-be-deleted user has no repositories.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str username: username of user to delete
        """
        path = "/admin/users/{}".format(username)
        self.delete(path, auth=auth)

    def get_repo_hooks(self, auth, username, repo_name):
        """
        Returns all hooks of repository with name ``repo_name`` owned by
        the user with username ``username``.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: name of repository
        :return: a list of hooks for the specified repository
        :rtype: List[GiteaRepo.Hooks]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}/hooks".format(u=username, r=repo_name)
        response = self.get(path, auth=auth)
        return [GiteaRepo.Hook.from_json(hook) for hook in response.json()]

    def create_hook(self, auth, repo_name, hook_type, config, events=None, organization=None, active=False):
        """
        Creates a new hook, and returns the created hook.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str repo_name: the name of the repo for which we create the hook
        :param str hook_type: The type of webhook, either "gitea", "gitea" or "slack"
        :param dict config: Settings for this hook (possible keys are
                            ``"url"``, ``"content_type"``, ``"secret"``)
        :param list events: Determines what events the hook is triggered for. Default: ["push"]
        :param str organization: Organization of the repo
        :param bool active: Determines whether the hook is actually triggered on pushes. Default is false
        :return: a representation of the created hook
        :rtype: GiteaRepo.Hook
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        if events is None:
            events = ["push"]  # default value is mutable, so assign inside body

        data = {
            "type": hook_type,
            "config": config,
            "events": events,
            "active": active
        }

        url = "/repos/{o}/{r}/hooks".format(o=organization, r=repo_name) if organization is not None \
            else "/repos/{r}/hooks".format(r=repo_name)
        response = self.post(url, auth=auth, data=data)
        return GiteaRepo.Hook.from_json(response.json())

    def update_hook(self, auth, repo_name, hook_id, update, organization=None):
        """
        Updates hook with id ``hook_id`` according to ``update``.

        :param auth.Authentication auth: authentication object
        :param str repo_name: repo of the hook to update
        :param int hook_id: id of the hook to update
        :param GiteaHookUpdate update: a ``GiteaHookUpdate`` object describing the requested update
        :param str organization: name of associated organization, if applicable
        :return: the updated hook
        :rtype: GiteaRepo.Hook
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        if organization is not None:
            path = "/repos/{o}/{r}/hooks/{i}".format(o=organization, r=repo_name, i=hook_id)
        else:
            path = "/repos/{r}/hooks/{i}".format(r=repo_name, i=hook_id)
        response = self._patch(path, auth=auth, data=update.as_dict())
        return GiteaRepo.Hook.from_json(response.json())

    def delete_hook(self, auth, username, repo_name, hook_id):
        """
        Deletes the hook with id ``hook_id`` for repo with name ``repo_name``
        owned by the user with username ``username``.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: name of repository of hook to delete
        :param int hook_id: id of hook to delete
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        path = "/repos/{u}/{r}/hooks/{i}".format(u=username, r=repo_name, i=hook_id)
        self.delete(path, auth=auth)

    def create_organization(self, auth, owner_name, org_name, full_name=None, description=None,
                            website=None, location=None):
        """
        Creates a new organization, and returns the created organization.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str owner_name: Username of organization owner
        :param str org_name: Organization name
        :param str full_name: Full name of organization 
        :param str description: Description of the organization
        :param str website: Official website
        :param str location: Organization location
        :return: a representation of the created organization
        :rtype: GiteaOrg
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        data = {
            "username": org_name,
            "full_name": full_name,
            "description": description,
            "website": website,
            "location": location
        }

        url = "/admin/users/{u}/orgs".format(u=owner_name)
        response = self.post(url, auth=auth, data=data)
        return GiteaOrg.from_json(response.json())

    def create_organization_team(self, auth, org_name, name, description=None, permission="read"):
        """
        Creates a new team of the organization.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str org_name: Organization user name
        :param str name: Full name of the team
        :param str description: Description of the team
        :param str permission: Team permission, can be read, write or admin, default is read
        :return: a representation of the created team
        :rtype: GiteaTeam
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        data = {
            "name": name,
            "description": description,
            "permission": permission
        }

        url = "/admin/orgs/{o}/teams".format(o=org_name)
        response = self.post(url, auth=auth, data=data)
        return GiteaTeam.from_json(response.json())

    def add_team_membership(self, auth, team_id, username):
        """
        Add user to team.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str team_id: Team's id
        :param str username: Username of the user to be added to team
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        url = "/admin/teams/{t}/members/{u}".format(t=team_id, u=username)
        self.put(url, auth=auth)

    def remove_team_membership(self, auth, team_id, username):
        """
        Remove user from team.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str team_id: Team's id
        :param str username: Username of the user to be removed from the team
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        url = "/admin/teams/{t}/members/{u}".format(t=team_id, u=username)
        self.delete(url, auth=auth)

    def add_repo_to_team(self, auth, team_id, repo_name):
        """
        Add or update repo from team.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str team_id: Team's id
        :param str repo_name: Name of the repo to be added to the team
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        url = "/admin/teams/{t}/repos/{r}".format(t=team_id, r=repo_name)
        self.put(url, auth=auth)

    def remove_repo_from_team(self, auth, team_id, repo_name):
        """
        Remove repo from team.

        :param auth.Authentication auth: authentication object, must be admin-level
        :param str team_id: Team's id
        :param str repo_name: Name of the repo to be removed from the team
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        url = "/admin/teams/{t}/repos/{r}".format(t=team_id, r=repo_name)
        self.delete(url, auth=auth)

    def list_deploy_keys(self, auth, username, repo_name):
        """
        List deploy keys for the specified repo.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: the name of the repo
        :return: a list of deploy keys for the repo
        :rtype: List[GiteaRepo.DeployKey]
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        response = self.get("/repos/{u}/{r}/keys".format(u=username, r=repo_name), auth=auth)
        return [GiteaRepo.DeployKey.from_json(key_json) for key_json in response.json()]

    def get_deploy_key(self, auth, username, repo_name, key_id):
        """
        Get a deploy key for the specified repo.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: the name of the repo
        :param int key_id: the id of the key
        :return: the deploy key
        :rtype: GiteaRepo.DeployKey
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        response = self.get("/repos/{u}/{r}/keys/{k}".format(u=username, r=repo_name, k=key_id), auth=auth)
        return GiteaRepo.DeployKey.from_json(response.json())

    def add_deploy_key(self, auth, username, repo_name, title, key_content):
        """
        Add a deploy key to the specified repo.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: the name of the repo
        :param str title: title of the key to add
        :param str key_content: content of the key to add
        :return: a representation of the added deploy key
        :rtype: GiteaRepo.DeployKey
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        data = {
            "title": title,
            "key": key_content
        }
        response = self.post("/repos/{u}/{r}/keys".format(u=username, r=repo_name), auth=auth, data=data)
        return GiteaRepo.DeployKey.from_json(response.json())

    def delete_deploy_key(self, auth, username, repo_name, key_id):
        """
        Remove deploy key for the specified repo.

        :param auth.Authentication auth: authentication object
        :param str username: username of owner of repository
        :param str repo_name: the name of the repo
        :param int key_id: the id of the key
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        self.delete("/repos/{u}/{r}/keys/{k}".format(u=username, r=repo_name, k=key_id), auth=auth)

    # Helper methods

    def _delete(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.delete(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def delete(self, path, auth=None, **kwargs):
        """
        Manually make a DELETE request.

        :param str path: relative url of the request (e.g. `/users/username`)
        :param auth.Authentication auth: authentication object
        :param kwargs dict: Extra arguments for the request, as supported by the
                            `requests <http://docs.python-requests.org/>`_ library.
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        return self._check_ok(self._delete(path, auth=auth, **kwargs))

    def _get(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.get(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def get(self, path, auth=None, **kwargs):
        """
        Manually make a GET request.

        :param str path: relative url of the request (e.g. `/users/username`)
        :param auth.Authentication auth: authentication object
        :param kwargs dict: Extra arguments for the request, as supported by the
                            `requests <http://docs.python-requests.org/>`_ library.
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        return self._check_ok(self._get(path, auth=auth, **kwargs))

    def _patch(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.patch(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def patch(self, path, auth=None, **kwargs):
        """
        Manually make a PATCH request.

        :param str path: relative url of the request (e.g. `/users/username`)
        :param auth.Authentication auth: authentication object
        :param kwargs dict: Extra arguments for the request, as supported by the
                            `requests <http://docs.python-requests.org/>`_ library.
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        return self._check_ok(self._patch(path, auth=auth, **kwargs))

    def _post(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.post(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def post(self, path, auth=None, **kwargs):
        """
        Manually make a POST request.

        :param str path: relative url of the request (e.g. `/users/username`)
        :param auth.Authentication auth: authentication object
        :param kwargs dict: Extra arguments for the request, as supported by the
                            `requests <http://docs.python-requests.org/>`_ library.
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        return self._check_ok(self._post(path, auth=auth, **kwargs))

    def _put(self, path, auth=None, **kwargs):
        if auth is not None:
            auth.update_kwargs(kwargs)
        try:
            return self._requestor.put(path, **kwargs)
        except requests.RequestException as exc:
            raise NetworkFailure(exc)

    def put(self, path, auth=None, **kwargs):
        """
        Manually make a PUT request.

        :param str path: relative url of the request (e.g. `/users/username`)
        :param auth.Authentication auth: authentication object
        :param kwargs dict: Extra arguments for the request, as supported by the
                            `requests <http://docs.python-requests.org/>`_ library.
        :raises NetworkFailure: if there is an error communicating with the server
        :raises ApiFailure: if the request cannot be serviced
        """
        return self._check_ok(self._put(path, auth=auth, **kwargs))

    @staticmethod
    def _check_ok(response):
        """
        Raise exception if response is non-OK, otherwise return response
        """
        if not response.ok:
            GiteaApi._fail(response)
        return response

    @staticmethod
    def _fail(response):
        """
        Raise an ApiFailure pertaining to the given response
        """
        message = "Status code: {}-{}, url: {}".format(response.status_code, response.reason, response.url)
        try:
            message += ", message:{}".format(response.json()["message"])
        except (ValueError, KeyError):
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
