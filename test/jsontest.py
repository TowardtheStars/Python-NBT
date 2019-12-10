import python_nbt.nbt as nbt
import json
import unittest

class JsonTest(unittest.TestCase):
    tag = nbt.read_from_nbt_file('test/test_read.nbt')
    json_path = 'test/test_json.json'

    def test1_to_json(self):
        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(self.tag.json_obj(), file, indent=2)

    def test2_from_json(self):
        with open(self.json_path) as file:
            _tag = nbt.from_json(json.load(file))
        self.assertEqual(self.tag, _tag)

unittest.main()
