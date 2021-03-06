
from utils.api_services import get_account_balance, get_account_statement
from utils.api_services import get_user_accounts


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
        self.currency_name = ""
        self.currency_plural = ""
        self.currency_symbol = ""
        self.currency_decimals = 0

    def get_balance(self, access):
        resp = get_account_balance(access, self.acc_link)
        self.balance = resp["data"]["attributes"]["balance"]
        self.currency_name = resp["included"][0]["attributes"]["name"]
        self.currency_plural = resp["included"][0]["attributes"]["namePlural"]
        self.currency_symbol = resp["included"][0]["attributes"]["symbol"]
        self.currency_decimals = resp["included"][0]["attributes"]["decimals"]

    def get_transfers(self, access):
        resp = get_account_statement(access, self.group_code, self.acc_id)
        transfers = []
        for trans in resp["data"]:
            if trans["type"] == "transfers":
                transfers.append(trans)
        return transfers
