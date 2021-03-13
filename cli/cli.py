import sys
import getpass

from core.oauth2 import ApiAccess
from core.account import get_user_accounts


class CommandLineInterface:
    def __init__(self, config):
        self.config = config
        self.access = None
        self.accounts = []
        self.account = None
        self.transfers = []

    def run(self):
        print("Connecting...", end='\r', flush=True)
        self.access = ApiAccess(self.config)
        self.access.get_local_auth()
        if not self.access.has_access:
            self._authenticate()
        self._get_accounts()
        self._get_transfers()

    def _authenticate(self):
        ok = False
        while not ok:
            message = _("Email")
            if self.access.user:
                message += " ({})".format(self.access.user)
            user_input = input("{}: ".format(message))
            password = getpass.getpass(_("Password") + ": ")
            user = user_input if user_input else self.access.user
            print(_("Authenticating") + "...", end='\r', flush=True)
            ok, error = self.access.new_access(user, password)
            if not ok:
                if error[0:17] == "Wrong credentials":
                    print(_("Wrong credentials"))
                if error[0:7] == "Network":
                    print(_("Network error"))
                    sys.exit()

    def _get_accounts(self):
        try:
            self.accounts = get_user_accounts(self.access)
        except Exception as e:
            print(str(e))
            sys.exit()
        self.account = self.accounts[0]
        print(_("Account") + ": {}".format(
              self.account.account["code"]) + " " * 10)
        print(_("Getting account info") + "...", end='\r', flush=True)
        try:
            self.account.get_balance(self.access)
        except Exception as e:
            print(str(e))
            sys.exit()
        print(_("Balance") + ": {} {}".format(
              self.account.balance,
              self.account.currency["symbol"]) + " " * 10)

    def _get_transfers(self):
        print(_("Getting last transactions") + "...", end='\r', flush=True)
        try:
            self.transfers = self.account.get_transfers(self.access)
        except Exception as e:
            print(str(e))
            sys.exit()
        for trans in self.transfers:
            print("{}| {}| {}".format(
                trans.created.strftime("%d/%m/%Y").ljust(10),
                trans.meta.ljust(40),
                "{} {}".format(trans.amount,
                               trans.currency["symbol"]).ljust(10)
            ))
