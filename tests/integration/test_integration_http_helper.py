import cloudpassage
import datetime
import hashlib
import os
import pytest


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


# This will make cleaning up easier...
content_prefix = '_SDK_test-'
content_name = str(content_prefix +
                   str(hashlib.md5(str(datetime.datetime.now())).hexdigest()))


class TestIntegrationGet:
    def test_get_404(self):
        endpoint = "/v1/barf"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.get(endpoint)
        assert '404' in str(e)

    def test_get_rekey(self):
        endpoint = "/v1/servers"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get(endpoint)
        assert "servers" in json_response


class TestIntegrationGetPaginated:
    def test_get_paginated_404(self):
        endpoint = "/v1/barf"
        key = "barfs"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.get_paginated(endpoint, key, pages)
        assert '404' in str(e)

    def test_get_paginated_rekey(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_events_99(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        req = cloudpassage.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_toomany(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 101
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            req.get_paginated(endpoint, key, pages)
        assert '100 max.' in str(e)

    def test_get_paginated_badkey(self):
        endpoint = "/v1/events"
        key = "badkey"
        pages = 2
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            req.get_paginated(endpoint, key, pages)
        assert key in str(e)


class TestIntegrationPost:
    def test_post_404(self):
        endpoint = "/v1/barf"
        post_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.post(endpoint, post_data)
        assert '404' in str(e)

    def test_post_bad_payload(self):
        endpoint = "/v1/groups"
        post_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            req.post(endpoint, post_data)
        assert '400' in str(e)

    def test_post_rekey(self):
        endpoint = "/v1/gropes"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.post(endpoint, {"nonexist": "nothing"})
        assert '404' in str(e)


class TestIntegrationPut:
    def test_put_bad_endpoint(self):
        endpoint = "/v1/barf"
        put_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.put(endpoint, put_data)
        assert '404' in str(e)

    def test_post_bad_payload(self):
        endpoint = "/v1/groups"
        put_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.put(endpoint, put_data)
        assert '404' in str(e)

    def test_put_rekey(self):
        body = {"server":
                {"retire": True}}
        endpoint = "/v1/servers/1234567890"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.put(endpoint, body)
        assert '404' in str(e)


class TestIntegrationDelete:
    def test_delete_404(self):
        endpoint = "/v1/barf"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.delete(endpoint)
        assert '404' in str(e)

    def test_delete_rekey(self):
        endpoint = "/v1/servers/123455432"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.delete(endpoint)
        assert '404' in str(e)
