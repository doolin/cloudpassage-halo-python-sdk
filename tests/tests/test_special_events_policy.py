import cloudpassage
import json
import os
import pytest

config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestSpecialEventsPolicy:
    def create_special_events_policy_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return cloudpassage.SpecialEventsPolicy(session)

    def test_instantiation(self):
        assert self.create_special_events_policy_obj()

    def test_list_all(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        se_policy = cloudpassage.SpecialEventsPolicy(session)
        se_policy_list = se_policy.list_all()
        assert "id" in se_policy_list[0]

    def test_create(self):
        rejected = False
        policy = self.create_special_events_policy_obj()
        try:
            policy.create("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_update(self):
        rejected = False
        policy = self.create_special_events_policy_obj()
        try:
            policy.update("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_describe(self):
        rejected = False
        policy = self.create_special_events_policy_obj()
        try:
            policy.describe("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_delete(self):
        rejected = False
        policy = self.create_special_events_policy_obj()
        try:
            policy.delete("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected
