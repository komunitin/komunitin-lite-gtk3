import sys, getpass, datetime

from utils.oauth2 import ApiAccess
from utils.api_services import get_user_accounts, get_account_balance
from utils.api_services import get_account_statement


def command_line_interface():
    user = ""
    print("Connecting...", end='\r', flush=True)
    access = ApiAccess()
    if not access.has_access:
        ok = False
        while not ok:
            user = access.user
            message_input = "Email: (" + user + "): " if user else "Email: "
            user_input = input(message_input)
            password = getpass.getpass()
            if user_input:
                user = user_input
            print("Authenticating...", end='\r', flush=True)
            ok, error = access.new_access(user, password)
            if not ok:
                if error == "Wrong credentials":
                    print(error)
                if error[0:7] == "Network":
                    print(error)
                    sys.exit()

    try:
        members, accounts, groups = get_user_accounts(access.headers)
    except Exception as e:
        print(str(e))
        sys.exit()
    print("Account: {}".format(members[0]["code"]) + " "*10)
    print("Getting account info...", end='\r', flush=True)
    try:
        balance, currency = get_account_balance(
            access.headers, groups[0]["code"], members[0]["code"])
    except Exception as e:
        print(str(e))
        sys.exit()
    print("Balance: {} {}".format(balance, currency["symbol"]) + " "*10)
    print("Getting last transactions...", end='\r', flush=True)
    try:
        transfers = get_account_statement(
            access.headers, groups[0]["code"], accounts[0]["id"])
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
