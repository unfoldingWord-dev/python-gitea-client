"""
Various classes representing update requests to Gitea
"""


class GiteaUserUpdate(object):
    """
    An immutable representation of a collection of Gitea user attributes to update.

    Instances should be created using the :class:`~GiteaUserUpdate.Builder` class.
    """

    def __init__(self, source_id, login_name, full_name, email, password, website,
                 location, active, admin, allow_git_hook, allow_import_local):
        self._source_id = source_id
        self._login_name = login_name
        self._full_name = full_name
        self._email = email
        self._password = password
        self._website = website
        self._location = location
        self._active = active
        self._admin = admin
        self._allow_git_hook = allow_git_hook
        self._allow_import_local = allow_import_local

    def as_dict(self):
        fields = {
            "source_id": self._source_id,
            "login_name": self._login_name,
            "full_name": self._full_name,
            "email": self._email,
            "password": self._password,
            "website": self._website,
            "location": self._location,
            "active": self._active,
            "admin": self._admin,
            "allow_git_hook": self._allow_git_hook,
            "allow_import_local": self._allow_import_local
        }
        return {k: v for (k, v) in fields.items() if v is not None}

    class Builder(object):
        def __init__(self, login_name, email):
            """
            :param str login_name: login name for authentication source
            :param str email: email address of user to update
            """
            self._source_id = None
            self._login_name = login_name
            self._full_name = None
            self._email = email
            self._password = None
            self._website = None
            self._location = None
            self._active = None
            self._admin = None
            self._allow_git_hook = None
            self._allow_import_local = None

        def set_source_id(self, source_id):
            """
            :param int source_id: Source id of authentication source

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._source_id = source_id
            return self

        def set_full_name(self, full_name):
            """
            :param str full_name: Updated full name for user

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._full_name = full_name
            return self

        def set_password(self, password):
            """
            :param str password: Updated password for user

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._password = password
            return self

        def set_website(self, website):
            """
            :param str website: Updated personal website for user

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._website = website
            return self

        def set_location(self, location):
            """
            :param str location: Updated location for user

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._location = location
            return self

        def set_active(self, active):
            """
            :param bool active: set true/false to signal that the updated user should be
                                activated/deactivated

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._active = active
            return self

        def set_admin(self, admin):
            """
            :param bool admin: whether the updated user should be admin

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._admin = admin
            return self

        def set_allow_git_hook(self, allow_git_hook):
            """
            :param bool allow_git_hook: whether the updated user should be allowed to use Git hooks

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._allow_git_hook = allow_git_hook
            return self

        def set_allow_import_local(self, allow_import_local):
            """

            :param bool allow_import_local: whether the updated user should be allowed to
                                            import local repositories

            :return: the updated builder
            :rtype: GiteaUserUpdate.Builder
            """
            self._allow_import_local = allow_import_local
            return self

        def build(self):
            """
            :return: A :class:`~GiteaUserUpdate` instance reflecting the changes added to the builder.
            :rtype: GiteaUserUpdate
            """
            return GiteaUserUpdate(
                source_id=self._source_id,
                login_name=self._login_name,
                full_name=self._full_name,
                email=self._email,
                password=self._password,
                website=self._website,
                location=self._location,
                active=self._active,
                admin=self._admin,
                allow_git_hook=self._allow_git_hook,
                allow_import_local=self._allow_import_local)


class GiteaHookUpdate(object):
    """
    An immutable representation of a collection of Gitea hook attributes to update.

    Instances should be created using the :class:`~GiteaHookUpdate.Builder` class.
    """

    def __init__(self, events, config, active):
        self._events = events
        self._config = config
        self._active = active

    def as_dict(self):
        fields = {
            "events": self._events,
            "config": self._config,
            "active": self._active,
        }
        return {k: v for (k, v) in fields.items() if v is not None}

    class Builder(object):
        def __init__(self):
            self._events = None
            self._config = None
            self._active = None

        def set_events(self, events):
            """
            :param List[str] events:
            :return: the updated builder
            :rtype: GiteaHookUpdate.Builder
            """
            self._events = events
            return self

        def set_config(self, config):
            """
            :param dict config:
            :return: the updated builder
            :rtype: GiteaHookUpdate.Builder
            """
            self._config = config
            return self

        def set_active(self, active):
            """
            :param bool active:
            :return: the updated builder
            :rtype: GiteaHookUpdate.Builder
            """
            self._active = active
            return self

        def build(self):
            """
            :return: A :class:`~GiteaHookUpdate` instance reflecting the changes added to the builder.
            :rtype: GiteaHookUpdate
            """
            return GiteaHookUpdate(
                events=self._events,
                config=self._config,
                active=self._active)
