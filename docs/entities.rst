Gitea Entities
==============

This page documents the classes provided by ``gitea_client`` module that represent entities
(e.g. users, repositories) in a `Gitea <https://gitea.io/>`_ server.

.. py:currentmodule:: gitea_client.entities

GiteaUser
---------

.. autoclass:: gitea_client.entities::GiteaUser()
    :members:

GiteaRepo
---------

.. autoclass:: gitea_client.entities::GiteaRepo()
    :members:

.. autoclass:: gitea_client.entities::GiteaRepo.Urls()
    :members:

.. autoclass:: gitea_client.entities::GiteaRepo.Permissions()
    :members:

.. autoclass:: gitea_client.entities::GiteaRepo.Hook()
    :members:

.. autoclass:: gitea_client.entities::GiteaRepo.DeployKey()
    :members:

GiteaOrg
--------

.. autoclass:: gitea_client.entities::GiteaOrg()
    :members:

GiteaTeam
---------

.. autoclass:: gitea_client.entities::GiteaTeam()
    :members:

GiteaBranch
-----------

.. autoclass:: gitea_client.entities::GiteaBranch()
    :members:

GiteaCommit
-----------

.. autoclass:: gitea_client.entities::GiteaCommit()
    :members:
