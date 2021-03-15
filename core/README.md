# Komunitin Lite Core

This is the main logic (UI agnostic). You can create new UIs using this core.

It works with three main objects:

- ApiAccess: it deals oauth2 authentication. Tries to read authentication from previous sessions (local_storage.py) or init new authentication.
  Public method: get_local_auth(), new_access(user, password)
  There's a function that returns all user accounts in a list: get_accounts(access) 
  
- Account: get all account data. 
  Public methods: get_balance(access), get_transfers(access), create_new_transfer()

- Transfer: get all transfer data. Send a new transfer to the server.
  Public methods: check_data(access), make_transfer(access)


A simple implementation:

    from core.oauth2 import ApiAccess
    from core.account import get_accounts
    
    access = ApiAccess(config)
    access.new_access("user", "password")  # fills in access object with headers
    accounts = get_accounts(access)  # this returns a list of account objects of the user
    account = accounts[0]
    print(account.account["code"])
    account.get_balance(access)  # fills in account object with balance and currency
    print("{} {}".format(account.balance, account.currency["name"]))
    transfers = account.get_transfers(access) # return a list of transfer objects
    for trans in transfers:
        print("{} {}".format(trans.amount, trans.currency["name"])


The methods that make calls to komunitin server must be async or in a new
thread, in order to maintain the UI not frozen.

