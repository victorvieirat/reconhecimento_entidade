import sys
import unittest
import json
from io import StringIO
from unittest.mock import patch

# Assuming the 'src' folder is one level above the 'test' folder
sys.path.append('./src')

import tratarInput


class TestReadJsonFile(unittest.TestCase):
    def test_read_valid_json_file(self):
        # Create a temporary JSON file with known content
        json_content = '{"key": "value", "numbers": [1, 2, 3]}'
        with patch('builtins.open', return_value=StringIO(json_content)):
            data = tratarInput.read_json_file('test.json')
            expected_data = json.loads(json_content)
            self.assertEqual(data, expected_data)

    def test_read_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            tratarInput.read_json_file('nonexistent_file.json')

    def test_read_invalid_json_file(self):
        # Create a temporary JSON file with invalid content
        invalid_json_content = '{"key": "value", "numbers": [1, 2, 3]'
        with patch('builtins.open', return_value=StringIO(invalid_json_content)):
            with self.assertRaises(json.JSONDecodeError):
                tratarInput.read_json_file('invalid.json')

if __name__ == '__main__':
    unittest.main()
