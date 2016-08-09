"""
Various classes representing update requests to Gogs
"""


class GogsUserUpdate(object):
    """
    An immutable represention of a collection of Gogs user attributes to update.

    Instances should be created using the :class:`~GogsUserUpdate.Builder` class.
    """
    def __init__(self, source_id, login_name, full_name, email, password, website,
                 location, active, admin, allow_git_hook, allow_import_local):
        """

        :param source_id:
        :param login_name:
        :param full_name:
        :param email:
        :param password:
        :param website:
        :param location:
        :param active:
        :param admin:
        :param allow_git_hook:
        :param allow_import_local:
        """

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
            :rtype: GogsUserUpdate.Builder
            """
            self._source_id = source_id
            return self

        def set_full_name(self, full_name):
            """
            :param str full_name: Updated full name for user

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._full_name = full_name
            return self

        def set_password(self, password):
            """
            :param str password: Updated password for user

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._password = password
            return self

        def set_website(self, website):
            """
            :param str website: Updated personal website for user

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._website = website
            return self

        def set_location(self, location):
            """
            :param str location: Updated location for user

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._location = location
            return self

        def set_active(self, active):
            """
            :param bool active: set true/false to signal that the updated user should be
                                activated/deactivated

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._active = active
            return self

        def set_admin(self, admin):
            """
            :param bool admin: whether the updated user should be admin

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._admin = admin
            return self

        def set_allow_git_hook(self, allow_git_hook):
            """
            :param bool allow_git_hook: whether the updated user should be allowed to use Git hooks

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._allow_git_hook = allow_git_hook
            return self

        def set_allow_import_local(self, allow_import_local):
            """

            :param bool allow_import_local: whether the updated user should be allowed to
                                            import local repositories

            :return: the updated builder
            :rtype: GogsUserUpdate.Builder
            """
            self._allow_import_local = allow_import_local
            return self

        def build(self):
            """
            :return: A :class:`~GogsUserUpdate` instance reflecting the changes added to the builder.
            :rtype: GogsUserUpdate
            """
            return GogsUserUpdate(
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
