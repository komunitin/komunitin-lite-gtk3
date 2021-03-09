import requests
from datetime import datetime
from .oauth2 import KomunitinNetError


def get_user_accounts(access):
    me_url = (access.server["base_api_url"] +
              "/social/users/me?include=members")
    resp = requests.get(me_url, headers=access.headers)
    if resp.status_code == 200:
        r = resp.json()
        data = {
            "user_id": r["data"]["id"],
            "accounts": []
        }
        for member in r["data"]["relationships"]["members"]["data"]:
            data["accounts"].append({
                "user_id": data["user_id"],
                "member_id": member["id"]
            })
        for i in r["included"]:
            if i["type"] == "members":
                for a in data["accounts"]:
                    if a["member_id"] == i["id"]:
                        a["member_name"] = i["attributes"]["name"]
                        a["member_image"] = i["attributes"]["image"]
                        a["acc_id"] = \
                            i["relationships"]["account"]["data"]["id"]
                        a["acc_code"] = i["attributes"]["code"]
                        a["acc_link"] = (i["relationships"]["account"]
                                         ["links"]["related"])
                        a["group_id"] = \
                            i["relationships"]["group"]["data"]["id"]
                        a["group_code"] = a["acc_link"].split("/")[-3]
        return data

    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_balance(access, acc_link):
    acc_url = "{}?{}".format(acc_link, "include=currency")
    resp = requests.get(acc_url, headers=access.headers)
    if resp.status_code == 200:
        r = resp.json()
        data = {
            "balance": r["data"]["attributes"]["balance"],
            "currency_id": r["included"][0]["id"],
            "currency_name": r["included"][0]["attributes"]["name"],
            "currency_plural": r["included"][0]["attributes"]["namePlural"],
            "currency_symbol": r["included"][0]["attributes"]["symbol"],
            "currency_decimals": r["included"][0]["attributes"]["decimals"],
        }
        return data
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_transfers(access, group_code, account_id):
    trans_url = (access.server["base_api_url"] + "/accounting/{}/transfers" +
                 "?filter[account]={}")
    resp = requests.get(trans_url.format(group_code, account_id),
                        headers=access.headers)
    if resp.status_code == 200:
        r = resp.json()
        data = []
        for t in r["data"]:
            if t["type"] == "transfers":
                trans = {
                    "transfer_id": t["id"],
                    "amount": t["attributes"]["amount"],
                    "meta": t["attributes"]["meta"],
                    "state": t["attributes"]["state"],
                    "created": datetime.fromisoformat(
                        t["attributes"]["created"]),
                    "updated": datetime.fromisoformat(
                        t["attributes"]["updated"]),
                    "payer_acc_id": t["relationships"]["payer"]["data"]["id"],
                    "payee_acc_id": t["relationships"]["payee"]["data"]["id"],
                    "currency_id": t["relationships"]["currency"]["data"]["id"]
                }
                data.append(trans)
        return data
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_unknown_accounts(access, group_code, account_ids):
    accounts_url = "{}/social/{}/members?filter[account]={}".format(
        access.server["base_api_url"], group_code, ','.join(account_ids))
    resp = requests.get(accounts_url, headers=access.headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def post_transfer(access, data):
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
