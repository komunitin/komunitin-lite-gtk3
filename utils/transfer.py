
from utils.api_services import check_account, post_transfer


class Transfer:
    def __init__(self, transfer_id=None):
        self.id = transfer_id
        self.amount = 0
        self.meta = ""
        self.state = ""
        self.created = ""
        self.updated = ""
        self.payer_account = {
            "id": "",
            "code": ""
        }
        self.payee_account = {
            "id": "",
            "code": ""
        }
        self.currency = {
            "id": "",
            "name": "",
            "plural": "",
            "symbol": "",
            "decimals": ""
        }

    def check_data(self, access):
        account_data = check_account(access, self.payer_account["code"])
        return True, None

    def make_transfer(self, access, data):
        data["from_account_id"] = self.acc_id
        resp = post_transfer(access, data)
