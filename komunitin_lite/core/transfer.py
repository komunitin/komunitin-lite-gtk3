
from komunitin_lite.core.api_services import check_account, post_transfer


class Transfer:
    def __init__(self, transfer_id=None):
        """Class Transfer
        constructor holding transfer_id and setting up all properties
        """
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

    def check_data(self, access, group_code):
        """Method to check if payer account exists and to get account id

        Parameters:
        access (ApiAccess object): needed to use auth headers
        Returns:
        boolean, str: True if exists, str with error if not
        """
        try:
            account_data = check_account(access, group_code,
                                         self.payer_account["code"])
        except Exception as e:
            return False, str(e)

        if account_data["currency_id"] != self.currency["id"]:
            return False, _("Cannot make a transfer in different currencies")

        self.payer_account["id"] = account_data["id"]
        return True, None

    def send_transfer(self, access, group_code):
        """Method to send completed transfer

        Parameters:
        access (ApiAccess object): needed to use auth headers
        Returns:
        boolean, str: True if done, str with error if not
        """
        amount = float(self.amount) * (10 ** int(self.currency["decimals"]))
        data = {
            "transaction_id": self.id,
            "group_code": group_code,
            "amount": int(amount),
            "meta": self.meta,
            "from_account_id": self.payer_account["id"],
            "to_account_id": self.payee_account["id"],
        }
        try:
            resp = post_transfer(access, data)
        except Exception as e:
            return False, str(e)

        # TODO assign missing data: created, state, etc...
        return True, ""
