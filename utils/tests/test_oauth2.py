import unittest
from unittest.mock import patch, mock_open
import configparser
import json

from utils.oauth2 import ApiAccess
from utils.local_storage import _encode, KOMUNITIN_DATA_FILE


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
        self.local_data["auth"]["created"] = 1614704597
        self.encoded_local_data = _encode("ofuscation",
                                          json.dumps(self.local_data))

    def test_init_ApiAccess(self):
        m = mock_open(read_data=self.encoded_local_data)
        with patch('utils.local_storage.open', m):
            self.access = ApiAccess(self.test_config)
        self.assertTrue(self.access.has_access is False)
        m.assert_called_once_with(KOMUNITIN_DATA_FILE, 'r')
        handle = m()
        handle.read.assert_called_once_with()

#    @patch('utils.oauth2.requests.post')
#    def test_new_access(self, fake_post):
#        fake_post.return_value.json.return_value = self.server_oauth2_response
#        m = mock_open()
#        with patch('utils.local_storage.open', m):
#            wrote = put_local_data(self.test_data)
#        self.assertTrue(wrote)
#        m.assert_called_once_with(KOMUNITIN_DATA_FILE, 'w')
#        handle = m()
#        handle.write.assert_called_once_with(self.encoded_data)


if __name__ == '__main__':
    unittest.main()
