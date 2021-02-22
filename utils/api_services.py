import requests
from .oauth2 import BASE_URL, KomunitinNetError


def get_user_accounts(headers):
    me_url = BASE_URL + \
      "/ces/api/social/users/me?include=members,members.account,members.group"
    members = []
    groups = []
    accounts = []
    resp = requests.get(me_url, headers=headers)
    if resp.status_code == 200:
        user_info = resp.json()
        for data in user_info['included']:
            if data['type'] == "members":
                member_data = data["attributes"]
                member_data["id"] = data["id"]
                members.append(member_data)
            elif data['type'] == "accounts":
                accounts.append({
                    "id": data["id"],
                    "link": data["links"]["self"]
                })
            elif data['type'] == "groups":
                groups_data = data["attributes"]
                groups_data["id"] = data["id"]
                groups.append(groups_data)
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)

    return members, accounts, groups


def get_account_balance(headers, group, account):
    acc_url = BASE_URL + \
      "/ces/api/accounting/{}/accounts/{}?include=currency"
    resp = requests.get(acc_url.format(group, account), headers=headers)
    if resp.status_code == 200:
        account_info = resp.json()

        balance = account_info["data"]["attributes"]["balance"]
        currency = account_info["included"][0]["attributes"]
        currency["id"] = account_info["included"][0]["id"]
        return balance, currency
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_statement(headers, group, account_id):
    trans_url = BASE_URL + \
      "/ces/api/accounting/{}/transfers?filter[account]={}"
    transfers = []
    resp = requests.get(trans_url.format(group, account_id), headers=headers)
    if resp.status_code == 200:
        trans_info = resp.json()
        for trans in trans_info["data"]:
            if trans["type"] == "transfers":
                transfers.append(trans)
        return transfers
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)

