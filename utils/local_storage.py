import os, json, base64

KOMUNITIN_DATA_FILE = os.path.join(os.path.expanduser("~"),
                                   '.komunitin_lite/data')
KOMUNITIN_CONFIG_FILE = os.path.join(os.path.expanduser("~"),
                                     '.komunitin_lite/config')


class KomunitinFileError(Exception):
    pass


def get_local_data(config=False):
    local_file = KOMUNITIN_CONFIG_FILE if config else KOMUNITIN_DATA_FILE
    return _read_data(local_file)


def put_local_data(komunitin_data, config=False):
    local_file = KOMUNITIN_CONFIG_FILE if config else KOMUNITIN_DATA_FILE
    return _write_data(komunitin_data, local_file)


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


def _read_data(local_file):
    komunitin_data = {}
    if os.path.isfile(local_file):
        try:
            with open(local_file, "r") as f:
                data = f.read()
            data = _decode("ofuscation", data)
            komunitin_data = json.loads(data)
        except Exception as e:
            print("Something wrong reading local data: %s" % e)
            raise KomunitinFileError(e)

    return komunitin_data


def _write_data(komunitin_data, local_file):

    # Only first time
    if not os.path.exists(os.path.dirname(local_file)):
        try:
            os.makedirs(os.path.dirname(local_file))
        except Exception as e:
            print("Something wrong creating local data directory: %s" % e)
            raise KomunitinFileError(e)

    try:
        data = json.dumps(komunitin_data)
        data = _encode("ofuscation", data)
        with open(local_file, "w") as f:
            f.write(data)
    except Exception as e:
        print("Something wrong writing local data: %s" % e)
        raise KomunitinFileError(e)

    return True
