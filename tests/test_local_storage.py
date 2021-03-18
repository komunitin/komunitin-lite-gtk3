import unittest
from unittest.mock import patch, mock_open
import json

from komunitin_lite.core.local_storage import (
    _encode, _decode, KOMUNITIN_DATA_FILE, KOMUNITIN_CONFIG_FILE,
    get_local_data, put_local_data)


class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "test_index": "test_data"
        }
        self.encoded_data = _encode("ofuscated", json.dumps(self.test_data))

    def test_encode(self):
        decoded_data = json.loads(_decode("ofuscated", self.encoded_data))
        self.assertTrue(self.test_data["test_index"] ==
                        decoded_data["test_index"])

    @patch('komunitin_lite.core.local_storage.os.path')
    def test_write_data(self, mock_path):
        mock_path.exists.return_value = True
        m = mock_open()
        with patch('komunitin_lite.core.local_storage.open', m):
            wrote = put_local_data(self.test_data)
        self.assertTrue(wrote)
        m.assert_called_once_with(KOMUNITIN_DATA_FILE, 'w')
        handle = m()
        handle.write.assert_called_once_with(self.encoded_data)

    @patch('komunitin_lite.core.local_storage.os.path')
    def test_read_data(self, mock_path):
        mock_path.isfile.return_value = True
        m = mock_open(read_data=self.encoded_data)
        with patch('komunitin_lite.core.local_storage.open', m):
            data_read = get_local_data()
        m.assert_called_once_with(KOMUNITIN_DATA_FILE, 'r')
        self.assertTrue(data_read == self.test_data)

    @patch('komunitin_lite.core.local_storage.os.path')
    def test_write_config(self, mock_path):
        mock_path.exists.return_value = True
        m = mock_open()
        with patch('komunitin_lite.core.local_storage.open', m):
            wrote = put_local_data(self.test_data, config=True)
        self.assertTrue(wrote)
        m.assert_called_once_with(KOMUNITIN_CONFIG_FILE, 'w')
        handle = m()
        handle.write.assert_called_once_with(json.dumps(self.test_data))

    @patch('komunitin_lite.core.local_storage.os.path')
    def test_read_config(self, mock_path):
        mock_path.isfile.return_value = True
        m = mock_open(read_data=json.dumps(self.test_data))
        with patch('komunitin_lite.core.local_storage.open', m):
            data_read = get_local_data(config=True)
        m.assert_called_once_with(KOMUNITIN_CONFIG_FILE, 'r')
        self.assertTrue(data_read == self.test_data)


if __name__ == '__main__':
    unittest.main()
