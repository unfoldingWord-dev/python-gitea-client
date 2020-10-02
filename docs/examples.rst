Examples
========

Example 1: Retrieving a repository
----------------------------------

Below is an example illustrating how to retrieve information about a repository::

    import gitea_client

    token = gitea_client.Token("my_token")
    username = "username"  # username of owner of repo
    repository_name = "repo_name"

    api = GiteaApi("https://try.gitea.io/")

    if not api.repo_exists(token, username, repository_name):
        print("Repository does not exist")
    else:
        repo = api.lookup_repo(token, username, repository_name)
        if repo.fork:
            print("Repository is a fork")
        else:
            print("Repository is not a fork")


Example 2: Updating a user
--------------------------

Below is an example demonstrating how to update a user (requires admin privileges)::

    import gitea_client

    login_name = "my_login"
    user_email = "user_to_update@example.com"

    update = gitea_client.GiteaUserUpdate.Builder(login_name, user_email)\
                .set_full_name("New Full Name")\
                .set_password("New Password")\
                .set_admin(False)\  # set the updated user as non-admin
                .build()

    api = gitea_client.GiteaApi("https://try.gitea.io/")
    api.update_user(
        gitea_client.Token("my_token"),  # must be admin
        "username_to_update",
        update)


Example 3: Creating a token
---------------------------

Below is an example illustrating how to create a token::

    import gitea_client

    api = gitea_client.GiteaApi("https://try.gitea.io/")

    auth = gitea_client.UsernamePassword("username", "password")
    token = api.create_token(auth, "my_token")

    print("token: {}, name: {}".format(token.token, token.name))
