from datetime import datetime

from utils.api_services import get_user_accounts, get_account_balance
from utils.api_services import get_account_transfers, get_unknown_accounts
from utils.transfer import Transfer


def get_accounts(access):
    resp = get_user_accounts(access)
    user_id = resp["data"]["id"]
    accounts = []
    for member in resp["data"]["relationships"]["members"]["data"]:
        accounts.append(Account(user_id, member["id"]))
    for incl in resp["included"]:
        if incl["type"] == "members":
            for a in accounts:
                if a.member_id == incl["id"]:
                    a.member_name = incl["attributes"]["name"]
                    a.member_image = incl["attributes"]["image"]
                    a.acc_id = incl["relationships"]["account"]["data"]["id"]
                    a.acc_code = incl["attributes"]["code"]
                    a.acc_link = \
                        incl["relationships"]["account"]["links"]["related"]
                    a.group_id = incl["relationships"]["group"]["data"]["id"]
                    a.group_code = a.acc_link.split("/")[-3]
    return accounts


class Account:
    def __init__(self, user_id, member_id):
        self.user_id = user_id
        self.member_id = member_id
        self.member_name = ""
        self.member_image = ""
        self.acc_id = ""
        self.acc_code = ""
        self.acc_link = ""
        self.group_id = ""
        self.group_code = ""
        self.balance = 0
        self.currency_id = ""
        self.currency_name = ""
        self.currency_plural = ""
        self.currency_symbol = ""
        self.currency_decimals = 0

    def get_balance(self, access):
        resp = get_account_balance(access, self.acc_link)
        self.balance = resp["data"]["attributes"]["balance"]
        self.currency_id = resp["included"][0]["id"]
        self.currency_name = resp["included"][0]["attributes"]["name"]
        self.currency_plural = resp["included"][0]["attributes"]["namePlural"]
        self.currency_symbol = resp["included"][0]["attributes"]["symbol"]
        self.currency_decimals = resp["included"][0]["attributes"]["decimals"]

    def get_transfers(self, access):
        resp = get_account_transfers(access, self.group_code, self.acc_id)
        transfers = []
        unknown_accounts = []
        for trans in resp["data"]:
            if trans["type"] == "transfers":
                t = Transfer(trans["id"])
                t.amount = trans["attributes"]["amount"]
                t.meta = trans["attributes"]["meta"]
                t.state = trans["attributes"]["state"]
                t.created = datetime.fromisoformat(
                    trans["attributes"]["created"])
                t.updated = datetime.fromisoformat(
                    trans["attributes"]["updated"])
                t.payer_acc_id = trans["relationships"]["payer"]["data"]["id"]
                if t.payer_acc_id == self.acc_id:
                    t.payer_acc_code = self.acc_code
                else:
                    unknown_accounts.append(t.payer_acc_id)
                t.payee_acc_id = trans["relationships"]["payee"]["data"]["id"]
                if t.payee_acc_id == self.acc_id:
                    t.payee_acc_code = self.acc_code
                else:
                    unknown_accounts.append(t.payee_acc_id)
                t.currency_id = self.currency_id
                t.currency_name = self.currency_name
                t.currency_plural = self.currency_plural
                t.currency_symbol = self.currency_symbol
                t.currency_decimals = self.currency_decimals
                transfers.append(t)
        # TODO: get unknown accounts
        # resp2 = get_unknown_accounts(access, self.group_code,
        #                              unknown_accounts)
        return transfers
