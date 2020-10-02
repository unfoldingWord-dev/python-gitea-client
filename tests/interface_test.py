import base64
import json
import unittest

import responses
from future.moves.urllib.parse import parse_qs

import gitea_client
import gitea_client._implementation.http_utils as http_utils


class GiteaClientInterfaceTest(unittest.TestCase):
    def setUp(self):
        self.api_endpoint = "https://www.example.com/api/v1/"
        self.base_url = "https://www.example.com/"
        self.client = gitea_client.GiteaApi(self.base_url)
        self.repo_json_str = """{
                "id": 27,
                "owner": {
                    "id": 1,
                    "username": "unknwon",
                    "full_name": "",
                    "email": "u@gitea.io",
                    "avatar_url": "/avatars/1"
                  },
                  "name": "Hello-World",
                  "full_name": "unknwon/Hello-World",
                  "description": "Some description",
                  "private": false,
                  "fork": false,
                  "parent": null,
                  "default_branch": "master",
                  "empty": false,
                  "size": 42,
                  "html_url": "http://localhost:3000/unknwon/Hello-World",
                  "clone_url": "http://localhost:3000/unknwon/hello-world.git",
                  "ssh_url": "jiahuachen@localhost:unknwon/hello-world.git",
                  "permissions": {
                    "admin": true,
                    "push": true,
                    "pull": true
                  }
                }"""
        self.repos_list_json_str = """[{
                "id": 27,
                "owner": {
                    "id": 1,
                    "username": "unknwon",
                    "full_name": "",
                    "email": "u@gitea.io",
                    "avatar_url": "/avatars/1"
                  },
                  "name": "Hello-World",
                  "full_name": "unknwon/Hello-World",
                  "description": "Some description",
                  "private": false,
                  "fork": false,
                  "parent": null,
                  "default_branch": "master",
                  "empty": false,
                  "size": 42,
                  "html_url": "http://localhost:3000/unknwon/Hello-World",
                  "clone_url": "http://localhost:3000/unknwon/hello-world.git",
                  "ssh_url": "jiahuachen@localhost:unknwon/hello-world.git",
                  "permissions": {
                    "admin": true,
                    "push": true,
                    "pull": true
                  }
                },{
                "id": 28,
                "owner": {
                    "id": 1,
                    "username": "unknwon",
                    "full_name": "",
                    "email": "u@gitea.io",
                    "avatar_url": "/avatars/1"
                  },
                  "name": "Hello-World-Again",
                  "full_name": "unknwon/Hello-World-Again",
                  "private": false,
                  "fork": false,
                  "parent": null,
                  "default_branch": "master",
                  "empty": false,
                  "size": 42,
                  "html_url": "http://localhost:3000/unknwon/Hello-World-Again",
                  "clone_url": "http://localhost:3000/unknwon/hello-world-again.git",
                  "ssh_url": "jiahuachen@localhost:unknwon/hello-world-again.git",
                  "permissions": {
                    "admin": true,
                    "push": true,
                    "pull": true
                  }
                }]"""
        self.branch_json_str = """{
                        "name": "master",
                        "commit": {
                            "id": "c17825309a0d52201e78a19f49948bcc89e52488",
                            "message": "migrated to RC0.2",
                            "url": "Not implemented",
                            "author": {
                                "name": "Joel Lonbeck",
                                "email": "joel@neutrinographics.com",
                                "username": "joel"
                            },
                            "committer": {
                                "name": "Joel Lonbeck",
                                "email": "joel@neutrinographics.com",
                                "username": "joel"
                            },
                            "verification": {
                                "verified": false,
                                "reason": "gpg.error.not_signed_commit",
                                "signature": "",
                                "payload": ""
                            },
                            "timestamp": "2017-05-17T21:11:25Z"
                            }
                        }"""
        self.branches_list_json_str = """[{
                        "name": "master",
                        "commit": {
                            "id": "c17825309a0d52201e78a19f49948bcc89e52488",
                            "message": "migrated to RC0.2",
                            "url": "Not implemented",
                            "author": {
                                "name": "Joel Lonbeck",
                                "email": "joel@neutrinographics.com",
                                "username": "joel"
                            },
                            "committer": {
                                "name": "Joel Lonbeck",
                                "email": "joel@neutrinographics.com",
                                "username": "joel"
                            },
                            "verification": {
                                "verified": false,
                                "reason": "gpg.error.not_signed_commit",
                                "signature": "",
                                "payload": ""
                            },
                            "timestamp": "2017-05-17T21:11:25Z"
                            }
                        },{
                        "name": "develop",
                        "commit": {
                            "id": "r03kd7cjr9a0d52201e78a19f49948bcc89e52488",
                            "message": "another branch",
                            "url": "Not implemented",
                            "author": {
                                "name": "Joel Lonbeck",
                                "email": "joel@neutrinographics.com",
                                "username": "joel"
                            },
                            "committer": {
                                "name": "Joel Lonbeck",
                                "email": "joel@neutrinographics.com",
                                "username": "joel"
                            },
                            "verification": {
                                "verified": false,
                                "reason": "gpg.error.not_signed_commit",
                                "signature": "",
                                "payload": ""
                            },
                            "timestamp": "2017-05-17T21:11:25Z"
                            }
                        }]"""
        self.user_json_str = """{
                  "id": 1,
                  "username": "unknwon",
                  "full_name": "",
                  "email": "u@gitea.io",
                  "avatar_url": "/avatars/1"
                }"""
        self.token_json_str = """{
                  "name": "new token",
                  "sha1": "mytoken"
                }"""
        self.username_password = gitea_client.UsernamePassword(
            "auth_username", "password")
        self.hook_json_str = """{
                "id": 4,
                "type": "gitea",
                "config": {
                  "content_type": "json",
                  "url": "http://test.io/hook"
                },
                "events": [
                  "create",
                  "push",
                  "issues"
                ],
                "active": false,
                "updated_at": "2017-03-31T12:42:58Z",
                "created_at": "2017-03-31T12:42:58Z"
              }"""
        self.hooks_list_json_str = """[
              {
                "id": 4,
                "type": "gitea",
                "config": {
                  "content_type": "json",
                  "url": "http://test.io/hook"
                },
                "events": [
                  "create",
                  "push",
                  "issues"
                ],
                "active": false,
                "updated_at": "2017-03-31T12:42:58Z",
                "created_at": "2017-03-31T12:42:58Z"
              },
              {
                "id": 3,
                "type": "gitea",
                "config": {
                  "content_type": "json",
                  "url": "http://192.168.201.1:8080/hook22/"
                },
                "events": [
                  "issue_comment"
                ],
                "active": true,
                "updated_at": "2017-03-31T12:47:56Z",
                "created_at": "2017-03-31T12:42:54Z"
              }
            ]"""
        self.org_json_str = """{
              "id": 7,
              "username": "gitea2",
              "full_name": "Gitea2",
              "avatar_url": "/avatars/7",
              "description": "Gitea is a painless self-hosted Git Service.",
              "website": "https://gitea.io",
              "location": "USA"
            }"""
        self.team_json_str = """{
              "id": 12,
              "name": "new-team",
              "description": "A new team created by API",
              "permission": "write"
            }"""
        self.deploy_key_json_str = """{
              "id": 1,
              "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUbmwBOG5vI8qNCztby5LDc9ozwTuwsqf+1fpuHjT9iQ2Lu9nlKHQJcPSgdrYAcc+88K6o74ayhTAjfajKxkIHnbzZFjidoVZSQDhX5qvl93jvY/Uz390qky0sweW+fspm8pRJL+ofE3QEN5AXAuycq1tgsRT32XC+Ta82Xyv8b3xW+pWbsZzYCzUsZXDe/xWxg1rndXh2BIrmcYf9BMiv9ZJIojJXfuLCeRXl550tDzaMFC0rQ/T5pZjs/lQemtg92MnxnEDi5nhuvDwM4Q8eqCTOXc4BCE7iyIHv+B7rx+0x99ytMh5BSIIGyWTfgTot/AjGVm5aRKJSRFgPBm9N comment with whitespace",
              "url": "http://localhost:3000/api/v1/repos/unknwon/project_x/keys/1",
              "title": "local",
              "created_at": "2015-11-18T15:05:43-05:00",
              "read_only": true
            }"""
        self.deploy_key_json_list = """[{
              "id": 1,
              "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUbmwBOG5vI8qNCztby5LDc9ozwTuwsqf+1fpuHjT9iQ2Lu9nlKHQJcPSgdrYAcc+88K6o74ayhTAjfajKxkIHnbzZFjidoVZSQDhX5qvl93jvY/Uz390qky0sweW+fspm8pRJL+ofE3QEN5AXAuycq1tgsRT32XC+Ta82Xyv8b3xW+pWbsZzYCzUsZXDe/xWxg1rndXh2BIrmcYf9BMiv9ZJIojJXfuLCeRXl550tDzaMFC0rQ/T5pZjs/lQemtg92MnxnEDi5nhuvDwM4Q8eqCTOXc4BCE7iyIHv+B7rx+0x99ytMh5BSIIGyWTfgTot/AjGVm5aRKJSRFgPBm9N comment with whitespace",
              "url": "http://localhost:3000/api/v1/repos/unknwon/project_x/keys/1",
              "title": "local",
              "created_at": "2015-11-18T15:05:43-05:00",
              "read_only": true
            },{
              "id": 2,
              "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUbmwBOG5vI8qNCztby5LDc9ozwTuwsqf+1fpuHjT9iQ2Lu9nlKHQJcPSgdrYAcc+88K6o74ayhTAjfajKxkIHnbzZFjidoVZSQDhX5qvl93jvY/Uz390qky0sweW+fspm8pRJL+ofE3QEN5AXAuycq1tgsRT32XC+Ta82Xyv8b3xW+pWbsZzYCzUsZXDe/xWxg1rndXh2BIrmcYf9BMiv9ZJIojJXfuLCeRXl550tDzaMFC0rQ/T5pZjs/lQemtg92MnxnEDi5nhuvDwM4Q8eqCTOXc4BCE7iyIHv+B7rx+0x99ytMh5BSIIGyWTfgTot/AjGVm5aRKJSRFgPBm9N comment with whitespace",
              "url": "http://localhost:3000/api/v1/repos/unknwon/project_x/keys/1",
              "title": "local",
              "created_at": "2015-11-18T15:05:43-05:00",
              "read_only": true
            }]"""
        self.expected_repo = gitea_client.GiteaRepo.from_json(json.loads(self.repo_json_str))
        self.expected_branch = gitea_client.GiteaBranch.from_json(json.loads(self.branch_json_str))
        self.expected_user = gitea_client.GiteaUser.from_json(json.loads(self.user_json_str))
        self.expected_hook = gitea_client.GiteaRepo.Hook.from_json(json.loads(self.hook_json_str))
        self.expected_org = gitea_client.GiteaOrg.from_json(json.loads(self.org_json_str))
        self.expected_team = gitea_client.GiteaTeam.from_json(json.loads(self.team_json_str))
        self.expected_key = gitea_client.GiteaRepo.DeployKey.from_json(json.loads(self.deploy_key_json_str))
        self.token = gitea_client.Token.from_json(json.loads(self.token_json_str))

    @responses.activate
    def test_create_repo1(self):
        uri = self.path("/user/repos")
        responses.add(responses.POST, uri, body=self.repo_json_str)
        repo = self.client.create_repo(self.token, "AGreatRepo")
        self.assert_repos_equal(repo, self.expected_repo)
        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0]
        self.assertEqual(call.request.url, self.path_with_token(uri))

    @responses.activate
    def test_repo_exists1(self):
        uri1 = self.path("/repos/username/repo1")
        uri2 = self.path("/repos/username/repo2")
        responses.add(responses.GET, uri1, body=self.repo_json_str, status=200)
        responses.add(responses.GET, uri2, status=404)
        self.assertTrue(self.client.repo_exists(self.token, "username", "repo1"))
        self.assertFalse(self.client.repo_exists(self.token, "username", "repo2"))
        self.assertEqual(len(responses.calls), 2)
        first_call = responses.calls[0]
        self.assertEqual(first_call.request.url, self.path_with_token(uri1))
        last_call = responses.calls[1]
        self.assertEqual(last_call.request.url, self.path_with_token(uri2))

    @responses.activate
    def test_get_repo1(self):
        uri1 = self.path("/repos/username/repo1")
        uri2 = self.path("/repos/username/repo2")
        responses.add(responses.GET, uri1, body=self.repo_json_str, status=200)
        responses.add(responses.GET, uri2, status=404)
        repo = self.client.get_repo(self.token, "username", "repo1")
        self.assert_repos_equal(repo, self.expected_repo)
        self.assertRaises(gitea_client.ApiFailure, self.client.get_repo,
                          self.token, "username", "repo2")
        self.assertEqual(len(responses.calls), 2)
        first_call = responses.calls[0]
        self.assertEqual(first_call.request.url, self.path_with_token(uri1))
        last_call = responses.calls[1]
        self.assertEqual(last_call.request.url, self.path_with_token(uri2))

    @responses.activate
    def test_get_user_repos(self):
        uri = self.path("/users/username/repos")
        responses.add(responses.GET, uri, body=self.repos_list_json_str, status=200)
        repos = self.client.get_user_repos(self.token, "username")
        self.assertEqual(len(repos), 2)
        self.assert_repos_equal(repos[0], self.expected_repo)

    @responses.activate
    def test_delete_repo1(self):
        uri1 = self.path("/repos/username/repo1")
        uri2 = self.path("/repos/otherusername/repo2")
        responses.add(responses.DELETE, uri1, status=204)
        responses.add(responses.DELETE, uri2, status=401)
        self.client.delete_repo(self.token, "username", "repo1")
        self.assertRaises(gitea_client.ApiFailure, self.client.delete_repo,
                          self.token, "otherusername", "repo2")
        self.assertEqual(len(responses.calls), 2)
        first_call = responses.calls[0]
        self.assertEqual(first_call.request.url, self.path_with_token(uri1))
        last_call = responses.calls[1]
        self.assertEqual(last_call.request.url, self.path_with_token(uri2))

    @responses.activate
    def test_get_branch(self):
        uri = self.path("/repos/username/repo/branches/branch")
        responses.add(responses.GET, uri, body=self.branch_json_str, status=200)
        branch = self.client.get_branch(self.token, "username", "repo", "branch")
        self.assert_branches_equal(branch, self.expected_branch)

    @responses.activate
    def test_get_branches(self):
        uri = self.path("/repos/username/repo/branches")
        responses.add(responses.GET, uri, body=self.branches_list_json_str, status=200)
        branches = self.client.get_branches(self.token, "username", "repo")
        self.assertEqual(len(branches), 2)
        self.assert_branches_equal(branches[0], self.expected_branch)

    @responses.activate
    def test_create_user1(self):
        uri = self.path("/admin/users")
        responses.add(responses.POST, uri, body=self.user_json_str, status=201)
        user = self.client.create_user(self.token, login_name="loginname",
                                       username="username", email="user@example.com",
                                       password="password")
        self.assert_users_equals(user, self.expected_user)
        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0]
        self.assertEqual(call.request.url, self.path_with_token(uri))

    @responses.activate
    def test_user_exists1(self):
        uri1 = self.path("/users/username1")
        uri2 = self.path("/users/username2")
        responses.add(responses.GET, uri1, body=self.user_json_str, status=200)
        responses.add(responses.GET, uri2, status=404)
        self.assertTrue(self.client.user_exists("username1"))
        self.assertFalse(self.client.user_exists("username2"))
        self.assertEqual(len(responses.calls), 2)
        first_call = responses.calls[0]
        self.assertEqual(first_call.request.url, uri1)
        last_call = responses.calls[1]
        self.assertEqual(last_call.request.url, uri2)

    @responses.activate
    def test_search_users(self):
        uri = self.path("/users/search")

        def callback(request):
            url = request.url
            index = url.find("?")
            self.assertTrue(index >= 0)  # assert a ? was actually found
            self.assertEqual(url[:index], uri)
            data = self.data_of_query(url[index + 1:])
            self.assertEqual(data["q"], "keyword")
            self.assertEqual(int(data["limit"]), 4)
            return 200, {}, "{\"data\": [%s], \"ok\": true}" % self.user_json_str

        responses.add_callback(responses.GET, uri, callback=callback)
        users = self.client.search_users("keyword", limit=4)
        self.assertEqual(len(users), 1)
        self.assert_users_equals(users[0], self.expected_user)

    @responses.activate
    def test_get_user1(self):
        uri1 = self.path("/users/username1")
        uri2 = self.path("/users/username2")
        responses.add(responses.GET, uri1, body=self.user_json_str, status=200)
        responses.add(responses.GET, uri2, status=404)
        user = self.client.get_user(None, "username1")
        self.assert_users_equals(user, self.expected_user)
        try:
            self.client.get_user(None, "username2")
            raise AssertionError("Call to get_user did not raise an exception")
        except gitea_client.ApiFailure as exc:
            self.assertIsNotNone(exc.message)
            self.assertEqual(exc.status_code, 404)
        self.assertEqual(len(responses.calls), 2)
        first_call = responses.calls[0]
        self.assertEqual(first_call.request.url, uri1)
        last_call = responses.calls[1]
        self.assertEqual(last_call.request.url, uri2)

    @responses.activate
    def test_update_user1(self):
        update = gitea_client.GiteaUserUpdate.Builder("loginname", "user@example.com") \
            .set_full_name("Example User") \
            .set_password("Password") \
            .set_website("mywebsite.net") \
            .set_active(True) \
            .set_admin(False) \
            .set_allow_git_hook(False) \
            .build()

        def callback(request):
            data = json.loads(request.body.decode('utf8'))
            self.assertEqual(data["login_name"], "loginname")
            self.assertEqual(data["full_name"], "Example User")
            self.assertEqual(data["email"], "user@example.com")
            self.assertEqual(data["password"], "Password")
            self.assertEqual(data["website"], "mywebsite.net")
            self.assertRegexpMatches(str(data["active"]), r"[tT]rue")
            self.assertRegexpMatches(str(data["admin"]), r"[fF]alse")
            self.assertRegexpMatches(str(data["allow_git_hook"]), r"[fF]alse")
            self.assertNotIn("id", data)
            self.assertNotIn("location", data)
            self.assertNotIn("allow_import_local", data)
            return 200, {}, self.user_json_str

        uri = self.path("/admin/users/username")
        responses.add_callback(responses.PATCH, uri, callback=callback)
        user = self.client.update_user(self.token, "username", update)
        self.assert_users_equals(user, self.expected_user)

    @responses.activate
    def test_delete_user1(self):
        uri1 = self.path("/admin/users/username1")
        uri2 = self.path("/admin/users/username2")
        responses.add(responses.DELETE, uri1, status=204)
        responses.add(responses.DELETE, uri2, status=401)
        self.client.delete_user(self.username_password, "username1")
        self.assertRaises(gitea_client.ApiFailure, self.client.delete_user,
                          self.username_password, "username2")
        self.assertEqual(len(responses.calls), 2)
        first_call = responses.calls[0]
        self.assertEqual(first_call.request.url, uri1)
        self.check_for_basic_auth(first_call.request)
        last_call = responses.calls[1]
        self.assertEqual(last_call.request.url, uri2)
        self.check_for_basic_auth(last_call.request)

    @responses.activate
    def test_valid_authentication1(self):
        uri = self.path("/user")
        valid_token = gitea_client.Token("a_valid_token")
        invalid_token = gitea_client.Token("an_invalid_token")

        def callback(request):
            if request.url == self.path_with_token(uri, valid_token):
                return 200, {}, self.user_json_str
            elif request.url == self.path_with_token(uri, invalid_token):
                return 401, {}, ""
            else:
                self.fail("Unexpected URL: {}".format(request.url))

        responses.add_callback(responses.GET, uri, callback=callback)
        self.assertTrue(self.client.valid_authentication(valid_token))
        self.assertFalse(self.client.valid_authentication(invalid_token))

    @responses.activate
    def test_authenticated_user(self):
        uri = self.path("/user")
        responses.add(responses.GET, uri, body=self.user_json_str, status=200)
        user = self.client.authenticated_user(self.token)
        self.assert_users_equals(user, self.expected_user)

    @responses.activate
    def test_ensure_token(self):
        uri = self.path("/users/{}/tokens".format(self.username_password.username))
        responses.add(responses.GET, uri, body="[]", status=200)
        responses.add(responses.POST, uri, body=self.token_json_str, status=200)
        responses.add(responses.GET, uri, body="[" + self.token_json_str + "]", status=200)
        token = self.client.ensure_token(self.username_password, self.token.name, self.username_password.username)
        self.assert_tokens_equals(token, self.token)
        token = self.client.ensure_token(self.username_password, self.token.name, self.username_password.username)
        self.assert_tokens_equals(token, self.token)

    @responses.activate
    def test_ensure_auth_token(self):
        uri = self.path("/user")
        responses.add(responses.GET, uri, body=self.user_json_str, status=200)
        uri = self.path("/users/{}/tokens".format(self.expected_user.username))
        responses.add(responses.GET, uri, body="[]", status=200)
        responses.add(responses.POST, uri, body=self.token_json_str, status=200)
        tokens = self.client.get_tokens(self.username_password)
        self.assertEqual(tokens, [])
        tokeninfo = self.client.create_token(self.username_password, self.token.name)
        self.assert_tokens_equals(tokeninfo, self.token)
        token = self.client.ensure_token(self.username_password, self.token.name)
        self.assert_tokens_equals(token, self.token)

    @responses.activate
    def test_create_hook1(self):
        uri = self.path("/repos/username/repo1/hooks")
        responses.add(responses.POST, uri, body=self.hook_json_str)
        hook = self.client.create_hook(self.token,
                                       repo_name="repo1",
                                       hook_type="gitea",
                                       config={
                                           "content_type": "json2",
                                           "url": "http://test.io/hook"
                                       },
                                       events=["create", "push", "issues"],
                                       active=False,
                                       organization="username")
        self.assert_hooks_equals(hook, self.expected_hook)
        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0]
        self.assertEqual(call.request.url, self.path_with_token(uri))

    @responses.activate
    def test_update_hook1(self):
        update = gitea_client.GiteaHookUpdate.Builder() \
            .set_events(["issues_comments"]) \
            .set_config({"url": "http://newurl.com/hook"}) \
            .set_active(True) \
            .build()

        def callback(request):
            data = json.loads(request.body.decode('utf8'))
            self.assertEqual(data["config"]["url"], "http://newurl.com/hook")
            self.assertEqual(data["events"], ['issues_comments'])
            self.assertEqual(data["active"], True)
            return 200, {}, self.hook_json_str

        uri = self.path("/repos/username/repo1/hooks/4")
        responses.add_callback(responses.PATCH, uri, callback=callback)
        hook = self.client.update_hook(self.token, "repo1", 4, update, organization="username")
        self.assert_hooks_equals(hook, self.expected_hook)

    @responses.activate
    def test_list_hooks(self):
        uri = self.path("/repos/username/repo1/hooks")
        responses.add(responses.GET, uri, body=self.hooks_list_json_str, status=200)
        hooks = self.client.get_repo_hooks(self.token, "username", "repo1")
        self.assertEqual(len(hooks), 2)
        self.assert_hooks_equals(hooks[0], self.expected_hook)

    @responses.activate
    def test_delete_hook(self):
        uri = self.path("/repos/username/repo1/hooks/4")
        responses.add(responses.DELETE, uri, status=204)
        hook = self.client.delete_hook(self.token, "username", "repo1", 4)
        self.assertEqual(hook, None)

    @responses.activate
    def test_create_organization(self):
        uri = self.path("/admin/users/username/orgs")
        responses.add(responses.POST, uri, body=self.org_json_str)
        org = self.client.create_organization(self.token,
                                              owner_name="username",
                                              org_name="gitea2",
                                              full_name="Gitea2",
                                              description="Gitea is a painless self-hosted Git Service.",
                                              website="https://gitea.io",
                                              location="USA")
        self.assert_org_equals(org, self.expected_org)
        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0]
        self.assertEqual(call.request.url, self.path_with_token(uri))

    @responses.activate
    def test_create_organization_team(self):
        uri = self.path("/admin/orgs/username/teams")
        responses.add(responses.POST, uri, body=self.team_json_str)
        team = self.client.create_organization_team(self.token,
                                                    org_name="username",
                                                    name="new-team",
                                                    description="A new team created by API",
                                                    permission="write")
        self.assert_team_equals(team, self.expected_team)
        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0]
        self.assertEqual(call.request.url, self.path_with_token(uri))

    @responses.activate
    def test_add_team_membership(self):
        uri = self.path("/admin/teams/team/members/username")
        responses.add(responses.PUT, uri, status=204)
        resp = self.client.add_team_membership(self.token, "team", "username")
        self.assertEqual(resp, None)

    @responses.activate
    def test_remove_team_membership(self):
        uri = self.path("/admin/teams/team/members/username")
        responses.add(responses.DELETE, uri, status=204)
        resp = self.client.remove_team_membership(self.token, "team", "username")
        self.assertEqual(resp, None)

    @responses.activate
    def test_add_repo_to_team(self):
        uri = self.path("/admin/teams/test_team/repos/repo_name")
        responses.add(responses.PUT, uri, status=204)
        resp = self.client.add_repo_to_team(self.token, "test_team", "repo_name")
        self.assertEqual(resp, None)

    @responses.activate
    def test_remove_repo_from_team(self):
        uri = self.path("/admin/teams/test_team/repos/repo_name")
        responses.add(responses.DELETE, uri, status=204)
        resp = self.client.remove_repo_from_team(self.token, "test_team", "repo_name")
        self.assertEqual(resp, None)

    @responses.activate
    def test_list_deploy_keys(self):
        uri = self.path("/repos/username/repo1/keys")
        responses.add(responses.GET, uri, body=self.deploy_key_json_list, status=200)
        keys = self.client.list_deploy_keys(self.token, "username", "repo1")
        self.assertEqual(len(keys), 2)
        self.assert_keys_equals(keys[0], self.expected_key)

    @responses.activate
    def test_delete_deploy_key(self):
        uri = self.path("/repos/username/repo1/keys/1")
        responses.add(responses.DELETE, uri, status=204)
        self.client.delete_deploy_key(self.token, "username", "repo1", 1)
        call = responses.calls[0]
        self.assertEqual(call.request.url, self.path_with_token(uri))

    @responses.activate
    def test_get_deploy_key(self):
        uri = self.path("/repos/username/repo1/keys/1")
        responses.add(responses.GET, uri, body=self.deploy_key_json_str)
        key = self.client.get_deploy_key(self.token, "username", "repo1", 1)
        self.assert_keys_equals(key, self.expected_key)

    @responses.activate
    def test_add_deploy_key(self):
        uri = self.path("/repos/username/repo1/keys")
        responses.add(responses.POST, uri, body=self.deploy_key_json_str)
        key_title = "My key title"
        key_content = "My key content"
        key = self.client.add_deploy_key(self.token, "username", "repo1", key_title, key_content)
        self.assert_keys_equals(key, self.expected_key)

    # helper methods

    @staticmethod
    def data_of_query(query):
        return {k: v[0] for (k, v) in parse_qs(query).items()}

    def path(self, relative):
        return http_utils.append_url(self.api_endpoint, relative)

    def path_with_token(self, path, token=None):
        token = self.token if token is None else token
        return "{p}?token={t}".format(p=path, t=token.token)

    def check_for_basic_auth(self, request):
        auth = "{u}:{p}".format(u=self.username_password.username,
                                p=self.username_password.password)
        b64 = base64.b64encode(auth.encode()).decode()
        self.assertEqual(request.headers["Authorization"], "Basic {}".format(b64))

    def assert_repos_equal(self, repo, expected):
        self.assertEqual(repo.id, expected.id)
        self.assert_users_equals(repo.owner, expected.owner)
        self.assertEqual(repo.full_name, expected.full_name)
        self.assertEqual(repo.private, expected.private)
        self.assertEqual(repo.fork, expected.fork)
        self.assertEqual(repo.parent, expected.parent)
        self.assertEqual(repo.default_branch, expected.default_branch)
        self.assertEqual(repo.size, expected.size)
        self.assertEqual(repo.empty, expected.empty)
        self.assertEqual(repo.urls.html_url, expected.urls.html_url)
        self.assertEqual(repo.urls.clone_url, expected.urls.clone_url)
        self.assertEqual(repo.urls.ssh_url, expected.urls.ssh_url)
        self.assertEqual(repo.permissions.admin, expected.permissions.admin)
        self.assertEqual(repo.permissions.push, expected.permissions.push)
        self.assertEqual(repo.permissions.pull, expected.permissions.pull)

    def assert_branches_equal(self, branch, expected):
        self.assertEqual(branch.name, expected.name)
        self.assert_commits_equal(branch.commit, expected.commit)

    def assert_commits_equal(self, commit, expected):
        self.assertEqual(commit.id, expected.id)
        self.assertEqual(commit.message, expected.message)
        self.assertEqual(commit.url, expected.url)
        self.assertEqual(commit.timestamp, expected.timestamp)

    def assert_users_equals(self, user, expected):
        self.assertEqual(user.id, expected.id)
        self.assertEqual(user.username, expected.username)
        self.assertEqual(user.full_name, expected.full_name)
        self.assertEqual(user.email, expected.email)
        self.assertEqual(user.avatar_url, expected.avatar_url)

    def assert_tokens_equals(self, token, expected):
        self.assertEqual(token.name, expected.name)
        self.assertEqual(token.token, expected.token)

    def assert_hooks_equals(self, hook, expected):
        self.assertEqual(hook.id, expected.id)
        self.assertEqual(hook.type, expected.type)
        self.assertEqual(hook.events, expected.events)
        self.assertEqual(hook.config, expected.config)
        self.assertEqual(hook.active, expected.active)

    def assert_org_equals(self, org, expected):
        self.assertEqual(org.id, expected.id)
        self.assertEqual(org.username, expected.username)
        self.assertEqual(org.full_name, expected.full_name)
        self.assertEqual(org.avatar_url, expected.avatar_url)
        self.assertEqual(org.description, expected.description)
        self.assertEqual(org.website, expected.website)
        self.assertEqual(org.location, expected.location)

    def assert_team_equals(self, team, expected):
        self.assertEqual(team.id, expected.id)
        self.assertEqual(team.name, expected.name)
        self.assertEqual(team.description, expected.description)
        self.assertEqual(team.permission, expected.permission)

    def assert_keys_equals(self, key, expected):
        self.assertEqual(key.id, expected.id)
        self.assertEqual(key.title, expected.title)
        self.assertEqual(key.url, expected.url)
        self.assertEqual(key.key, expected.key)
        self.assertEqual(key.read_only, expected.read_only)
        self.assertEqual(key.created_at, expected.created_at)


if __name__ == "__main__":
    unittest.main()
