import uuid

from komunitin_lite.core.api_services import (
    get_user_accounts, get_account_balance, get_account_transfers,
    get_unknown_accounts)
from komunitin_lite.core.transfer import Transfer


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

        accounts_info = get_unknown_accounts(access, self.group["code"],
                                             unknown_accounts)
        # TODO: optimize this if possible
        for i in range(0, len(transfers)):
            for a_info in accounts_info:
                if transfers[i].payer_account["id"] == a_info["id"]:
                    transfers[i].payer_account["code"] = a_info["code"]
                    break
                elif transfers[i].payee_account["id"] == a_info["id"]:
                    transfers[i].payee_account["code"] = a_info["code"]
                    break

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
