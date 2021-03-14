
CONFIG_SERVER = {
    'server_name': 'test.server.com',
    'base_api_url': 'https://test.server.com/ces/api',
    'oauth2_token_url': 'https://test.server.com/oauth2/token',
    'oauth2_client_id': 'test-client-id',
    'oauth2_client_password': 'test-client-password',
    'oauth2_scope': 'test-scope test-scope2',
}

SERVER_OAUTH2_RESPONSE = {
    'access_token': 'ba6a3dfa96c6f5862cc944f36e55f3e9d9a767e1',
    'expires_in': 3600, 'token_type': 'Bearer',
    'scope': 'test-scope test-scope2',
    'refresh_token': '7da4b334f3484c245206ea9ccd528548e405423c',
}


class FakeApiAccess:
    def __init__(self, config):
        self.server = config["server"]
        self.has_access = True
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer ba6a3dfa96c6f5862cc944f36e55f3e9d9a767e1'
        }
        self.user = "user@test.server.com"
        self._auth = SERVER_OAUTH2_RESPONSE
