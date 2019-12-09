import python_nbt.nbt as nbt
import json
import unittest

class ReadFileTest(unittest.TestCase):

    tag = nbt.read_from_nbt_file('test/test_read.nbt')

    def test_byte(self):
        self.assertEqual(self.tag['tag_type'], 10, 'Byte test')

    def test_short(self):
        self.assertEqual(self.tag['nbt_version'], 19133)

    def test_int(self):
        self.assertEqual(self.tag['int_tag'], 1048576)

    def test_long(self):
        self.assertEqual(self.tag['long_tag'], 1510346461649)
    
    def test_float(self):
        self.assertEqual(self.tag['float_tag'], 2.71828)
    
    def test_double(self):
        self.assertEqual(self.tag['pi'], 3.14159265358975)

    def test_bytearray(self):
        self.assertListEqual(self.tag['bytes_helloworld'], list(b'Hello, world!'))
    
    def test_intarray(self):
        self.assertListEqual(self.tag['int_array'], [
            1048576,
            2097152,
            4194304,
            8388608,
            16777216  
        ])

    def test_longarray(self):
        self.assertListEqual(self.tag['long_array'],[
            1111111111111111111,
            2222222222222222222,
            3333333333333333333  
        ])

    def test_taglist(self):
        self.assertListEqual(self.tag['description'].value, list(map(nbt.NBTTagString, ['Python-NBT test', 'Created on 2019/12/09'])))

    def test_compound(self):
        self.assertEqual(self.tag['test_version']['major'], 0)
        self.assertEqual(self.tag['test_version']['minor'], 0)
        self.assertEqual(self.tag['test_version']['build'], 1)

    def test_nesting(self):
        nested = self.tag['multi_nesting']
        for i in range(1, 5):
            nested = nested['layer' + str(i)]
        self.assertEqual(nested['yay'], 'yay!')


class WriteFileTest(unittest.TestCase):

    tag = ReadFileTest.tag

    def test_write(self):
        nbt.write_to_nbt_file('test/test_write.nbt', self.tag)
        


unittest.main()

