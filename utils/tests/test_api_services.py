import unittest
from unittest.mock import Mock, patch
import configparser

from utils.api_services import (get_user_accounts, get_account_balance,
                                get_account_statement)
from utils.tests.fake_objects import (CONFIG_SERVER, FakeApiAccess,
                                      ME_RESPONSE, BALANCE_RESPONSE,
                                      STATEMENT_RESPONSE)


class TestApiServices(unittest.TestCase):
    def setUp(self):
        self.test_config = configparser.ConfigParser()
        self.test_config['server'] = CONFIG_SERVER
        self.access = FakeApiAccess(self.test_config)
        self.me_response = ME_RESPONSE
        self.balance_response = BALANCE_RESPONSE
        self.statement_response = STATEMENT_RESPONSE

    @patch('utils.api_services.requests.get')
    def test_user_accounts(self, mock_get):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = self.me_response
        mock_get.return_value = response_mock
        members, accounts, groups = get_user_accounts(self.access)
        self.assertTrue(accounts[0]["id"] ==
                        'a383a9dc-7ad4-4868-8807-069675c6ad3e')
        response_mock.json.return_value = self.balance_response
        mock_get.return_value = response_mock
        balance, currency = get_account_balance(self.access,
                                                groups[0], accounts[0])
        self.assertTrue(balance == 130)

        response_mock.json.return_value = self.statement_response
        mock_get.return_value = response_mock
        transfers = get_account_statement(self.access, groups[0],
                                          accounts[0]["id"])
        self.assertTrue(transfers[0]["id"] ==
                        'e2f52ef0-6deb-471a-aeb3-ea10a1b187e2')


if __name__ == '__main__':
    unittest.main()
