Gogs Entities
=============

This page documents the classes provided by ``gogs_client`` module that represent entities
(e.g. users, repositories) in a `Gogs <https://gogs.io/>`_ server.

.. py:currentmodule:: gogs_client.entities

GogsUser
--------

.. autoclass:: gogs_client.entities::GogsUser()

    .. autoattribute:: id
        :annotation:

    .. autoattribute:: username
        :annotation:

    .. autoattribute:: email
        :annotation:

    .. autoattribute:: full_name
        :annotation:

    .. autoattribute:: avatar_url
        :annotation:

GogsRepo
--------

.. autoclass:: gogs_client.entities::GogsRepo()
    :members:

.. autoclass:: gogs_client.entities::GogsRepo.Urls()
    :members:

.. autoclass:: gogs_client.entities::GogsRepo.Permissions()
    :members:

.. autoclass:: gogs_client.entities::GogsRepo.Hook()
    :members:

.. autoclass:: gogs_client.entities::GogsRepo.DeployKey()
    :members:

GogsOrg
-------

.. autoclass:: gogs_client.entities::GogsOrg()
    :members:

GogsTeam
--------

.. autoclass:: gogs_client.entities::GogsTeam()
    :members:
