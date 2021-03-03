import unittest
from unittest.mock import Mock, patch
import configparser
import time

from utils.oauth2 import ApiAccess


class TestOauth2(unittest.TestCase):
    def setUp(self):
        self.access = None
        self.test_config = configparser.ConfigParser()
        self.test_config['server'] = {
            'server_name': 'test.server.com',
            'base_api_url': 'https://test.server.com/ces/api',
            'oauth2_token_url': 'https://test.server.com/oauth2/token',
            'oauth2_client_id': 'test-client-id',
            'oauth2_client_password': 'test-client-password',
            'oauth2_scope': 'test-scope test-scope2',
        }
        self.server_oauth2_response = {
            'access_token': 'ba6a3dfa96c6f5862cc944f36e55f3e9d9a767e1',
            'expires_in': 3600, 'token_type': 'Bearer',
            'scope': 'test-scope test-scope2',
            'refresh_token': '7da4b334f3484c245206ea9ccd528548e405423c',
        }
        self.local_data = {
            'user': 'user@test.server.com',
            'auth': self.server_oauth2_response
        }
        self.local_data["auth"]["created"] = int(time.time())

    @patch('utils.local_storage.get_local_data')
    def test_init_no_data(self, mock_get_data):
        mock_get_data.return_value = {}
        self.access = ApiAccess(self.test_config)
        self.assertTrue(self.access.has_access is False)

    @patch('utils.oauth2.requests.post')
    @patch('utils.oauth2.put_local_data')
    @patch('utils.oauth2.get_local_data')
    def test_init_with_data(self, mock_get_data, mock_put_data, mock_post):
        mock_get_data.return_value = self.local_data
        mock_put_data.return_value = True
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = self.server_oauth2_response
        mock_post.return_value = response_mock
        self.access = ApiAccess(self.test_config)
        self.assertTrue(self.access.has_access is True)


if __name__ == '__main__':
    unittest.main()
