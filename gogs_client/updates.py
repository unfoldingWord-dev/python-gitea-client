"""
Various classes representing update requests to Gogs
"""


class GogsUserUpdate(object):
    """
    Represents a collections of Gogs user attributes to update
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
            self._source_id = source_id
            return self

        def set_full_name(self, full_name):
            self._full_name = full_name
            return self

        def set_password(self, password):
            self._password = password
            return self

        def set_website(self, website):
            self._website = website
            return self

        def set_location(self, location):
            self._location = location
            return self

        def set_active(self, active):
            self._active = active
            return self

        def set_admin(self, admin):
            self._admin = admin
            return self

        def set_allow_git_hook(self, allow_git_hook):
            self._allow_git_hook = allow_git_hook

        def set_allow_import_local(self, allow_import_local):
            self._allow_import_local = allow_import_local

        def build(self):
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
