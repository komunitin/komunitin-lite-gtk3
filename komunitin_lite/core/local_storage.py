import os
import json
import base64
import logging

USER_LOCAL_DIR = os.path.join(os.path.expanduser("~"), '.komunitin_lite')
KOMUNITIN_DATA_FILE = os.path.join(USER_LOCAL_DIR, 'data')
KOMUNITIN_CONFIG_FILE = os.path.join(USER_LOCAL_DIR, 'config')

logger = logging.getLogger('KomLite')

class KomunitinFileError(Exception):
    pass


def get_local_data(config=False):
    if config:
        data = _read_data(KOMUNITIN_CONFIG_FILE, ofuscated=False)
        logger.debug('Config data read from user local storage')
    else:
        data = _read_data(KOMUNITIN_DATA_FILE)
        logger.debug('Auth data read from user local storage')

    return data


def put_local_data(data, config=False):
    if config:
        done = _write_data(data, KOMUNITIN_CONFIG_FILE, ofuscated=False)
        logger.debug('Config data written to user local storage')
    else:
        done = _write_data(data, KOMUNITIN_DATA_FILE)
        logger.debug('Auth data written to user local storage')

    return done


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


def _read_data(local_file, ofuscated=True):
    komunitin_data = {}
    if os.path.isfile(local_file):
        try:
            with open(local_file, "r") as f:
                data = f.read()
            if ofuscated:
                data = _decode("ofuscated", data)
            komunitin_data = json.loads(data)
        except Exception as e:
            logger.error("Something wrong reading local data: {}".format(e))
            raise KomunitinFileError(e)

    return komunitin_data


def _write_data(komunitin_data, local_file, ofuscated=True):
    try:
        data = json.dumps(komunitin_data)
        if ofuscated:
            data = _encode("ofuscated", data)
        with open(local_file, "w") as f:
            f.write(data)
    except Exception as e:
        logger.error("Something wrong writting local data: {}".format(e))
        raise KomunitinFileError(e)

    return True
