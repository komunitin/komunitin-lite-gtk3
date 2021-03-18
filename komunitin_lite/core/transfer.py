
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

    def check_data(self, access):
        """Method to check if payer account exists and to get account id

        Parameters:
        access (ApiAccess object): needed to use auth headers
        Returns:
        boolean, str: True if exists, str with error if not
        """
        account_data = check_account(access, self.payer_account["code"])
        # TODO assign payer account id, check currency, etc...
        return True, None

    def make_transfer(self, access):
        """Method to send completed transfer

        Parameters:
        access (ApiAccess object): needed to use auth headers
        Returns:
        boolean, str: True if done, str with error if not
        """
        # TODO prepare data
        data = {}
        resp = post_transfer(access, data)
        # TODO assign missing data: created, state, etc...
        return True, ""
