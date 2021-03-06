import requests
from .oauth2 import KomunitinNetError


def get_user_accounts(access):
    me_url = (access.server["base_api_url"] +
              "/social/users/me?include=members")
    resp = requests.get(me_url, headers=access.headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_balance(access, acc_link):
    acc_url = "{}?{}".format(acc_link, "include=currency")
    resp = requests.get(acc_url, headers=access.headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_statement(access, group_code, account_id):
    trans_url = (access.server["base_api_url"] + "/accounting/{}/transfers" +
                 "?filter[account]={}")
    resp = requests.get(trans_url.format(group_code, account_id),
                        headers=access.headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def put_transfer(access, data):
    transfer_url = "{}/accounting/{}/transfers".format(
        access.server["api_base_url"], data["currency"])
    body = {
        "data": {
            "id": data["transaction_id"],
            "type": "transfers",
            "attributes": {
                "amount": data["amount"],
                "meta": data["meta"],
                "state": "committed"
            },
            "relationships": {
                "payer": {
                    "data": {
                        "type": "accounts",
                        "id": data["from_account_id"]
                    }
                },
                "payee": {
                    "data": {
                        "type": "accounts",
                        "id": data["to_account_id"]
                    }
                }
            }
        }
    }
    resp = requests.post(transfer_url, body=body, headers=access.headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)
