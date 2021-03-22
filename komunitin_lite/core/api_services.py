import requests
from datetime import datetime

from komunitin_lite.core.oauth2 import KomunitinNetError


def get_user_accounts(access):
    me_url = (access.server["base_api_url"] +
              "/social/users/me?include=members")
    resp = requests.get(me_url, headers=access.headers, timeout=5)
    if resp.status_code == 200:
        r = resp.json()
        data = {
            "user_id": r["data"]["id"],
            "accounts": []
        }
        for member in r["data"]["relationships"]["members"]["data"]:
            data["accounts"].append({
                "user": {"id": data["user_id"]},
                "member": {"id": member["id"]},
                "account": {},
                "group": {},
                "balance": 0,
                "currency": {}
            })
        for i in r["included"]:
            if i["type"] == "members":
                for a in data["accounts"]:
                    if a["member"]["id"] == i["id"]:
                        a["member"]["name"] = i["attributes"]["name"]
                        a["member"]["image"] = i["attributes"]["image"]
                        a["account"]["id"] = \
                            i["relationships"]["account"]["data"]["id"]
                        a["account"]["code"] = i["attributes"]["code"]
                        a["account"]["link"] = (i["relationships"]["account"]
                                                ["links"]["related"])
                        a["group"]["id"] = \
                            i["relationships"]["group"]["data"]["id"]
                        a["group"]["code"] = \
                            a["account"]["link"].split("/")[-3]
        return data

    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_balance(access, acc_link):
    acc_url = "{}?{}".format(acc_link, "include=currency")
    resp = requests.get(acc_url, headers=access.headers, timeout=5)
    if resp.status_code == 200:
        r = resp.json()
        data = {
            "balance": r["data"]["attributes"]["balance"],
            "currency": {
                "id": r["included"][0]["id"],
                "name": r["included"][0]["attributes"]["name"],
                "plural": r["included"][0]["attributes"]["namePlural"],
                "symbol": r["included"][0]["attributes"]["symbol"],
                "decimals": r["included"][0]["attributes"]["decimals"],
            }
        }
        return data
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_account_transfers(access, group_code, account_id):
    trans_url = (access.server["base_api_url"] + "/accounting/{}/transfers" +
                 "?filter[account]={}")
    resp = requests.get(trans_url.format(group_code, account_id),
                        headers=access.headers, timeout=5)
    if resp.status_code == 200:
        r = resp.json()
        data = []
        for t in r["data"]:
            if t["type"] == "transfers":
                trans = {
                    "id": t["id"],
                    "amount": t["attributes"]["amount"],
                    "meta": t["attributes"]["meta"],
                    "state": t["attributes"]["state"],
                    "created": datetime.fromisoformat(
                        t["attributes"]["created"]),
                    "updated": datetime.fromisoformat(
                        t["attributes"]["updated"]),
                    "payer_account": {
                        "id": t["relationships"]["payer"]["data"]["id"],
                        "code": ""
                    },
                    "payee_account": {
                        "id": t["relationships"]["payee"]["data"]["id"],
                        "code": ""
                    },
                    "currency": {
                        "id": t["relationships"]["currency"]["data"]["id"]
                    }
                }
                data.append(trans)
        return data
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def get_unknown_accounts(access, group_code, account_ids):
    accounts_url = "{}/social/{}/members?filter[account]={}".format(
        access.server["base_api_url"], group_code, ','.join(account_ids))
    resp = requests.get(accounts_url, headers=access.headers, timeout=5)
    if resp.status_code == 200:
        members = resp.json()
        accounts_info = []
        for a_id in account_ids:
            for memb in members["data"]:
                if memb["relationships"]["account"]["data"]["id"] == a_id:
                    accounts_info.append({
                        "id": a_id,
                        "code": memb["attributes"]["code"],
                        "name": memb["attributes"]["name"],
                    })

        return accounts_info

    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def check_account(access, network_code, account_code):
    account_url = "{}/accounting/{}/accounts/{}".format(
        access.server["base_api_url"], network_code, account_code)
    resp = requests.get(account_url, headers=access.headers, timeout=5)
    if resp.status_code == 200:
        data = resp.json()["data"]
        return {
            "id": data["id"],
            "code": data["attributes"]["code"],
            "currency_id": data["relationships"]["currency"]["data"]["id"],
        }

    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)


def post_transfer(access, data):
    transfer_url = "{}/accounting/{}/transfers".format(
        access.server["base_api_url"], data["currency_id"])
    params = {
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
    resp = requests.post(transfer_url, params, headers=access.headers,
                         timeout=5)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Error %s: %s" % (resp.status_code, resp.text))
        raise KomunitinNetError(resp.text, resp.status_code)
