import unittest
from unittest.mock import patch, mock_open
import json

from utils.local_storage import _encode, _decode, KOMUNITIN_DATA_FILE
from utils.local_storage import get_local_data, put_local_data


class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "test_index": "test_data"
        }
        self.encoded_data = _encode("ofuscation", json.dumps(self.test_data))

    def test_encode(self):
        decoded_data = json.loads(_decode("ofuscation", self.encoded_data))
        self.assertTrue(self.test_data["test_index"] ==
                        decoded_data["test_index"])

    def test_write_data(self):
        m = mock_open()
        with patch('utils.local_storage.open', m):
            wrote = put_local_data(self.test_data)
        self.assertTrue(wrote)
        m.assert_called_once_with(KOMUNITIN_DATA_FILE, 'w')
        handle = m()
        handle.write.assert_called_once_with(self.encoded_data)

    def test_read_data(self):
        m = mock_open(read_data=self.encoded_data)
        with patch('utils.local_storage.open', m):
            data_read = get_local_data()
        self.assertTrue(data_read == self.test_data)
        m.assert_called_once_with(KOMUNITIN_DATA_FILE, 'r')
        handle = m()
        handle.read.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
