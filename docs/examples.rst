Examples
========

Example 1: Retrieving a repository
----------------------------------

Below is an example illustrating how to retrieve information about a repository::

    import gogs_client

    token = gogs_client.Token("my_token")
    username = "username"  # username of owner of repo
    repository_name = "repo_name"

    api = GogsApi("https://try.gogs.io/")

    if not api.repo_exists(token, username, repository_name):
        print("Repository does not exist")
    else:
        repo = api.lookup_repo(token, username, repository_name)
        if repo.fork:
            print("Repository is a fork")
        else:
            print("Repository is not a fork")


Example 2: Updating a User
--------------------------

Below is an example demonstrating how to update a user (requires admin privileges)::

    import gogs_client

    login_name = "my_login"
    user_email = "user_to_update@example.com"

    update = gogs_client.GogsUserUpdate.Builder(login_name, user_email)\
                .set_full_name("New Full Name")\
                .set_password("New Password")\
                .set_admin(False)\  # set the updated user as non-admin
                .build()

    api = gogs_client.GogsApi("https://try.gogs.io/")
    api.update_user(
        gogs_client.Token("my_token"),  # must be admin
        "username_to_update",
        update)

