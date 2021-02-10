import requests
from .oauth2 import BASE_URL, KomunitinNetError


def get_account_info(headers):
    me_url = BASE_URL + "/ces/api/social/users/me?include=account"
    acc_url = BASE_URL + "/ces/api/accounting/accounts?filter&account={}"
    account_id = ""
    accounts = []

    resp1 = requests.get(me_url, headers=headers)
    if resp1.status_code == 200:
        user_info = resp1.json()
        account_id = user_info['data']['id']
    else:
        print("Error %s: %s" % (resp1.status_code, resp1.text))
        raise KomunitinNetError(resp1.text, resp1.status_code)

    if account_id:
        resp2 = requests.get(acc_url.format(account_id), headers=headers)
        if resp2.status_code == 200:
            accounts_info = resp2.json()
            accounts = [acc['id'] for acc in accounts_info['data']]

    return accounts[0] if accounts else account_id
