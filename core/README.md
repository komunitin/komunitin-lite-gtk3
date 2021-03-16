# Komunitin Lite Core

This is the main logic (GUI agnostic). You can create a new GUI using this core.

It works with three main objects:

- ApiAccess: oauth2 authentication. Tries to read authentication from previous session or a new authentication.
  Public methods: get_local_auth(), new_access(user, password)
  
- Account: account management. 
  Public methods: get_balance(access), get_transfers(access), create_new_transfer()
  There's a function that returns all user accounts in a objects list: get_accounts(access) 

- Transfer: transfer management.
  Public methods: check_data(access), make_transfer(access)


A simple implementation to see last transfers of an account:

    from core.oauth2 import ApiAccess
    from core.account import get_accounts
    
    access = ApiAccess(config)
    access.new_access("user", "password")  # fills in access object with token and headers
    accounts = get_accounts(access)  # returns a list of account objects of the user
    account = accounts[0]
    print(account.account["code"])
    account.get_balance(access)  # fills in account object with balance and currency
    print("{} {}".format(account.balance, account.currency["name"]))
    transfers = account.get_transfers(access) # return a list of transfer objects
    for trans in transfers:
        print("{} {}".format(trans.amount, trans.currency["name"])


The methods that make calls to komunitin server must be async or in a new
thread, in order to maintain the GUI not frozen.

