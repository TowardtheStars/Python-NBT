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

    def test3_to_simple_json(self):
        self.assertDictEqual(self.tag.json_obj(full_json=False),
            {
                "long_array":[
                    1111111111111111111,
                    2222222222222222222,
                    3333333333333333333
                ],
                "nbt_version": 19133,
                "description": [
                    "Python-NBT test",
                    "Created on 2019/12/09"
                ],
                "pi": 3.141592653589746,
                "int_array":[
                    1048576,
                    2097152,
                    4194304,
                    8388608,
                    16777216
                ],
                "test_version":{
                    "major":0,
                    "minor":0,
                    "build":1
                },
                "bytes_helloworld":[
                    72,
                    101,
                    108,
                    108,
                    111,
                    44,
                    32,
                    119,
                    111,
                    114,
                    108,
                    100,
                    33
                ],
                "int_tag":1048576,
                "tag_type":10,
                "long_tag":1510346461649,
                "float_tag":2.718280076980591,
                "multi_nesting":{
                    "layer1":{
                        "layer2":{
                            "layer3":{
                                "layer4":{
                                    "yay":"yay!"
                                }
                            }
                        }
                    }
                }
            }
        )
unittest.main()
