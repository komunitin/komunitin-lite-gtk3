import uuid

from core.api_services import get_user_accounts, get_account_balance
from core.api_services import get_account_transfers  # , get_unknown_accounts
from core.transfer import Transfer


def get_accounts(access):
    data = get_user_accounts(access)
    accounts = []
    for account in data["accounts"]:
        account_obj = Account(data["user_id"])
        for key, value in account.items():
            setattr(account_obj, key, value)
        accounts.append(account_obj)

    return accounts


class Account:
    def __init__(self, user_id):
        """Class Account
        constructor holding user_id and setting up all properties
        """
        self.user = {"id": user_id}
        self.member = {
            "id": "",
            "name": "",
            "image": ""
        }
        self.account = {
            "id": "",
            "code": "",
            "link": ""
        }
        self.group = {
            "id": "",
            "code": ""
        }
        self.balance = 0
        self.currency = {
            "id": "",
            "name": "",
            "plural": "",
            "symbol": "",
            "decimals": 0
        }

    def get_balance(self, access):
        """Method to read balance and currency of the account

        Parameters:
        access (ApiAccess object): needed to use auth headers
        Returns:
        nothing (just fill in some object properties)
        """
        data = get_account_balance(access, self.account["link"])
        for key, value in data.items():
            setattr(self, key, value)

    def get_transfers(self, access):
        """Method to read last transfers of the account
           (it needs to make a second call for unknown accounts)

        Parameters:
        access (ApiAccess object): needed to use auth headers
        Returns:
        A list of Transfer objects
        """
        data = get_account_transfers(access, self.group["code"],
                                     self.account["id"])
        transfers = []
        unknown_accounts = []
        for trans in data:
            t = Transfer(trans["id"])
            for key, value in trans.items():
                setattr(t, key, value)
            if t.payer_account["id"] == self.account["id"]:
                t.payer_account["code"] = self.account["code"]
            else:
                unknown_accounts.append(t.payer_account["id"])
            if t.payee_account["id"] == self.account["id"]:
                t.payee_account["code"] = self.account["code"]
            else:
                unknown_accounts.append(t.payee_account["id"])
            if t.currency["id"] == self.currency["id"]:
                t.currency = self.currency

            transfers.append(t)

        # TODO: get unknown accounts
        # resp2 = get_unknown_accounts(access, self.group_code,
        #                              unknown_accounts)
        return transfers

    def create_new_transfer(self, from_account, amount, meta):
        """Method to create a new transfer object with account object data

        Parameters:
        from_account: str (account code)
        amount: float
        meta: str (concept of new transfer)
        Return:
        Transfer object
        """
        trans = Transfer(str(uuid.uuid4()))
        trans.amount = amount
        trans.meta = meta
        trans.payer_account = {
            "id": "",
            "code": from_account
        }
        trans.payee_account = {
            "id": self.account["id"],
            "code": self.account["code"]
        }
        trans.currency = self.currency
        return trans
