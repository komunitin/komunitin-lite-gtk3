import unittest
from unittest import mock
import json

from utils.local_storage import _encode, _decode


class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        self.readdata_patcher = mock.patch('utils.local_storage._read_data')
        self.readdata_patcher.start()
        self.writedata_patcher = mock.patch('utils.local_storage._write_data')
        self.writedata_patcher.start()

    def test_encode(self):
        test_data = {
            "test_index": "test_data"
        }
        encoded_data = _encode("ofuscation", json.dumps(test_data))
        decoded_data = json.loads(_decode("ofuscation", encoded_data))
        self.assertTrue(test_data["test_index"] == decoded_data["test_index"])

    def test_write_read_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
