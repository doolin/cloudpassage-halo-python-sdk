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


class TestSystemAnnouncement:
    def create_announcement(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return(cloudpassage.SystemAnnouncement(session))

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.SystemAnnouncement(session)

    def test_list_all(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        announcement = cloudpassage.SystemAnnouncement(session)
        announcement_list = announcement.list_all()
        assert "announcement" in announcement_list[0]
