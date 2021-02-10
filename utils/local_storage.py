import os, time, json, base64

KOMUNITIN_FILE = os.path.join(os.path.expanduser("~"), '.komunitin')


class KomunitinFileError(Exception):
    pass


def _encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def _decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def get_local_data():
    komunitin_data = {}
    if os.path.isfile(KOMUNITIN_FILE):
        try:
            with open(KOMUNITIN_FILE, "r") as f:
                data = f.read()
            data = _decode("ofuscation", data)
            komunitin_data =  json.loads(data)
        except Exception as e:
            print("Something wrong reading local data: %s" % e)
            raise KomunitinFileError(e)

    if komunitin_data:
        if "user" in komunitin_data and "auth" in komunitin_data:
            return komunitin_data["user"], komunitin_data["auth"]

    return "", ""

def put_local_data(user, auth):
    if "created" not in auth:
        auth["created"] = int(time.time())
    komunitin_data = {
        "user": user,
        "auth": auth
    }
    try:
        data = json.dumps(komunitin_data)
        data = _encode("ofuscation", data)
        with open(KOMUNITIN_FILE, "w") as f:
            f.write(data)
    except Exception as e:
        print("Something wrong writing local data: %s" % e)
        raise KomunitinFileError(e)
