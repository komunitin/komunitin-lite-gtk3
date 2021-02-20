import time, requests
from .local_storage import get_local_data, put_local_data, KomunitinFileError

OAUTH_CLIENT_ID = "odoo-pos-komunitin"
OAUTH_SCOPE = "komunitin_accounting komunitin_social profile"
BASE_URL = "https://demo.integralces.net"
token_url = BASE_URL + "/oauth2/token"


class KomunitinNetError(Exception):
    def __init__(self, message, status_code=0):
        super().__init__(message)
        self.status_code = status_code


class KomunitinAuthError(Exception):
    pass


class ApiAccess:

    def __init__(self):
        self.has_access = False
        self.headers = {}
        try:
            self.user, self._auth = get_local_data()
        except KomunitinFileError:
            self.user = ""
            self._auth = {}

        if self._auth:
            # check if token is expired
            expire = int(self._auth["created"]) + int(self._auth["expires_in"])
            if int(time.time()) > expire:
                # expired token.
                self._auth = {}
            else:
                # valid token, so refresh it.
                try:
                    self._refresh_auth_token()
                except (KomunitinNetError,
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.ConnectionError):
                    self._auth = {}
                except KomunitinFileError:
                    pass

    def new_access(self, user, password):
        # Try to authenticate and get token.
        error = ""
        try:
            self._get_auth_token(user, password)
        except KomunitinAuthError:
            self.has_access = False
            error = "Wrong credentials"
        except (KomunitinNetError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError) as e:
            self.access = False
            error = 'Network Error: {}'.format(e)
        except KomunitinFileError:
            self.access = True

        return self.has_access, error

    def _get_auth_token(self, user, password):
        params = {
            "grant_type": "password",
            "username": user,
            "password": password,
            "client_id": OAUTH_CLIENT_ID,
            "scope": OAUTH_SCOPE
        }
        response = requests.post(token_url, params, timeout=5)
        if response.status_code == 200:
            self.user = user
            self._auth = response.json()
            self.has_access = True
            self.headers = self._make_headers(self._auth['access_token'])
            put_local_data(self.user, self._auth)
        elif response.status_code == 401:
            # Authentication fail
            self.has_access = False
            raise KomunitinAuthError(response.text)
        else:
            print("Error %s: %s" % (response.status_code, response.text))
            raise KomunitinNetError(response.text, response.status_code)

    def _refresh_auth_token(self):
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self._auth["refresh_token"],
            "username": self.user,
            "client_id": OAUTH_CLIENT_ID,
            "scope": OAUTH_SCOPE
        }
        response = requests.post(token_url, params, timeout=5)
        if response.status_code == 200:
            print("Token refreshed", end='\r', flush=True)
            self.has_access = True
            self._auth = response.json()
            self.headers = self._make_headers(self._auth['access_token'])
            put_local_data(self.user, self._auth)
        else:
            print("Error %s: %s" % (response.status_code, response.text))
            raise KomunitinNetError(response.text, response.status_code)

    def _make_headers(self, token):
        return {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer ' + token
        }
