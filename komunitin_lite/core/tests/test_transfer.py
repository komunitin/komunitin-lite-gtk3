import unittest
from unittest.mock import Mock, patch
import configparser
import json
import os

from komunitin_lite.core.account import get_accounts
from komunitin_lite.core.tests.fake_objects import CONFIG_SERVER, FakeApiAccess


class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.test_config = configparser.ConfigParser()
        self.test_config['server'] = CONFIG_SERVER
        self.access = FakeApiAccess(self.test_config)
        di = os.path.dirname(__file__)
        with open(os.path.join(di, 'json/oauth2_response.json'), 'r') as f:
            self.access._auth = json.load(f)
        with open(os.path.join(di, 'json/me_response.json'), 'r') as f:
            self.me_response = json.load(f)
        with open(os.path.join(di, 'json/balance_response.json'), 'r') as f:
            self.balance_response = json.load(f)
        with open(os.path.join(di, 'json/transfers_response.json'), 'r') as f:
            self.transfers_response = json.load(f)

    @patch('core.api_services.requests.get')
    def test_tranfer(self, mock_get):
        # get_accounts
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = self.me_response
        mock_get.return_value = response_mock
        accounts = get_accounts(self.access)
        self.assertTrue(len(accounts) == 2)
        self.assertTrue(accounts[0].account["code"] == "NET20000")

        # account.get_balance
        self.account = accounts[0]
        response_mock.json.return_value = self.balance_response
        mock_get.return_value = response_mock
        self.account.get_balance(self.access)
        self.assertTrue(self.account.balance == 130)

        # account.create_new_transfer
        new_trans = self.account.create_new_transfer("TEST0000", 12, "test")
        self.assertTrue(new_trans.payee_account["code"] == "NET20000")
        self.assertTrue(new_trans.currency["name"] == "eco")

        # transfer.check_data
        # TODO

        # transfer.make_transfer
        # TODO


if __name__ == '__main__':
    unittest.main()
