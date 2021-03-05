import sys
import getpass
import datetime

from utils.oauth2 import ApiAccess
from utils.api_services import get_user_accounts, get_account_balance
from utils.api_services import get_account_statement


def command_line_interface(config):
    print("Connecting...", end='\r', flush=True)
    access = ApiAccess(config)
    if not access.has_access:
        _authenticate(access)
    try:
        members, accounts, groups = get_user_accounts(access)
    except Exception as e:
        print(str(e))
        sys.exit()
    print(_("Account") + ": {}".format(members[0]["code"]) + " "*10)
    print(_("Getting account info") + "...", end='\r', flush=True)
    try:
        balance, currency = get_account_balance(
            access, groups[0]["code"], members[0]["code"])
    except Exception as e:
        print(str(e))
        sys.exit()
    print(_("Balance") + ": {} {}".format(
        balance, currency["symbol"]) + " "*10)
    print(_("Getting last transactions") + "...", end='\r', flush=True)
    try:
        transfers = get_account_statement(
            access, groups[0]["code"], accounts[0]["id"])
    except Exception as e:
        print(str(e))
        sys.exit()
    for trans in transfers:
        created = datetime.datetime.fromisoformat(
            trans["attributes"]["created"])
        amount = str(trans["attributes"]["amount"]) + " " + currency["symbol"]
        print("{}| {}| {}".format(
            created.strftime("%d/%m/%Y").ljust(10),
            trans["attributes"]["meta"].ljust(40),
            amount.ljust(10)
        ))


def _authenticate(access):
    ok = False
    while not ok:
        message = _("Email")
        message += " (" + access.user + "): " if access.user else ": "
        user_input = input(message)
        password = getpass.getpass(_("Password") + ": ")
        if user_input:
            user = user_input
        print(_("Authenticating") + "...", end='\r', flush=True)
        ok, error = access.new_access(user, password)
        if not ok:
            if error[0:17] == "Wrong credentials":
                print(_("Wrong credentials"))
            if error[0:7] == "Network":
                print(_("Network error"))
                sys.exit()
