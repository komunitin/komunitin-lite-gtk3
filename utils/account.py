from utils.api_services import get_user_accounts, get_account_balance
from utils.api_services import get_account_transfers  # , get_unknown_accounts
from utils.transfer import Transfer


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
        self.user_id = user_id
        self.member_id = ""
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
        data = get_account_balance(access, self.acc_link)
        for key, value in data.items():
            setattr(self, key, value)

    def get_transfers(self, access):
        data = get_account_transfers(access, self.group_code, self.acc_id)
        transfers = []
        unknown_accounts = []
        for trans in data:
            t = Transfer(trans["transfer_id"])
            for key, value in trans.items():
                setattr(t, key, value)
            if t.payer_acc_id == self.acc_id:
                t.payer_acc_code = self.acc_code
            else:
                unknown_accounts.append(t.payer_acc_id)
            if t.payee_acc_id == self.acc_id:
                t.payee_acc_code = self.acc_code
            else:
                unknown_accounts.append(t.payee_acc_id)
            if t.currency_id == self.currency_id:
                t.currency_name = self.currency_name
                t.currency_plural = self.currency_plural
                t.currency_symbol = self.currency_symbol
                t.currency_decimals = self.currency_decimals
            else:
                # transfer currency is not the same as account.
                # could this happen ??
                pass

            transfers.append(t)

        # TODO: get unknown accounts
        # resp2 = get_unknown_accounts(access, self.group_code,
        #                              unknown_accounts)
        return transfers
