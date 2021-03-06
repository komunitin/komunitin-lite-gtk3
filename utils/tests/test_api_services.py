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
        resp = get_user_accounts(self.access)
        included = resp["included"][0]
        account_id = included["relationships"]["account"]["data"]["id"]
        account_code = included["attributes"]["code"]
        account_link = included["relationships"]["account"]["links"]["related"]
        self.assertTrue(account_code == 'NET20000')
        response_mock.json.return_value = self.balance_response
        mock_get.return_value = response_mock
        resp = get_account_balance(self.access, account_link)
        balance = resp["data"]["attributes"]["balance"]
        self.assertTrue(balance == 130)

        response_mock.json.return_value = self.statement_response
        mock_get.return_value = response_mock
        group_code = account_link.split("/")[-3]
        transfers = get_account_statement(self.access, group_code,
                                          account_id)
        self.assertTrue(transfers["data"][0]["id"] ==
                        'e2f52ef0-6deb-471a-aeb3-ea10a1b187e2')


if __name__ == '__main__':
    unittest.main()
