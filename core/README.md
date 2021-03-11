# Komunitin Lite Core

This is the main logic (UI agnostic). You can create new UIs using this core.

It works with three main objects:

- ApiAccess: it deals oauth2 authentication. Tries to read authentication from previous sessions (local_storage.py) or init new authentication.
  Public method: new_access(user, password)
  
- Account: get all account data. 
  Public methods: get_balance(access), get_transfers(access), create_new_transfer()

- Transfer: get all transfer data.
  Public methods: check_data(access), make_transfer(access)

See cli/cli.py for a simple implementation.

