
from utils.api_services import post_transfer


class Transfer:
    def __init__(self, transfer_id=None):
        self.transfer_id = transfer_id
        self.amount = ""
        self.meta = ""
        self.state = ""
        self.created = ""
        self.updated = ""
        self.payer_acc_id = ""
        self.payer_acc_code = ""
        self.payee_acc_id = ""
        self.payee_acc_code = ""
        self.currency_id = ""
        self.currency_name = ""
        self.currency_plural = ""
        self.currency_symbol = ""
        self.currency_decimals = ""

    def check_transfer(self, access, data):
        pass

    def make_transfer(self, access, data):
        data["from_account_id"] = self.acc_id
        resp = post_transfer(access, data)
