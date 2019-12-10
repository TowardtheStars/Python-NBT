import python_nbt.nbt as nbt
import json
import unittest

def approx(var1, var2, delta):
    return abs(var1 - var2) <= abs(delta)

class ReadFileTest(unittest.TestCase):

    tag = nbt.read_from_nbt_file('test/test_read.nbt')

    def test_byte(self):
        self.assertEqual(self.tag['tag_type'].value, 10, 'Byte test')

    def test_short(self):
        self.assertEqual(self.tag['nbt_version'].value, 19133)

    def test_int(self):
        self.assertEqual(self.tag['int_tag'].value, 1048576)

    def test_long(self):
        self.assertEqual(self.tag['long_tag'].value, 1510346461649)
    
    def test_float(self):
        self.assertTrue(approx(self.tag['float_tag'].value, 2.71828, 0.000005))
    
    def test_double(self):
        self.assertTrue(approx(self.tag['pi'].value, 3.141592653589746, 0.0000000000000005))

    def test_bytearray(self):
        self.assertListEqual(self.tag['bytes_helloworld'].value, list(b'Hello, world!'))
    
    def test_intarray(self):
        self.assertListEqual(self.tag['int_array'].value, [
            1048576,
            2097152,
            4194304,
            8388608,
            16777216  
        ])

    def test_longarray(self):
        self.assertListEqual(self.tag['long_array'].value,[
            1111111111111111111,
            2222222222222222222,
            3333333333333333333  
        ])

    def test_taglist(self):
        self.assertListEqual(self.tag['description'].value, list(map(nbt.NBTTagString, ['Python-NBT test', 'Created on 2019/12/09'])))

    def test_compound(self):
        self.assertEqual(self.tag['test_version']['major'].value, 0)
        self.assertEqual(self.tag['test_version']['minor'].value, 0)
        self.assertEqual(self.tag['test_version']['build'].value, 1)

    def test_nesting(self):
        nested = self.tag['multi_nesting']
        for i in range(1, 5):
            nested = nested['layer' + str(i)]
        self.assertEqual(nested['yay'].value, 'yay!')


class WriteFileTest(unittest.TestCase):

    tag = ReadFileTest.tag

    def test_write(self):
        nbt.write_to_nbt_file('test/test_write.nbt', self.tag)
        read_tag = nbt.read_from_nbt_file('test/test_write.nbt')
        self.assertEqual(read_tag, self.tag)
        

unittest.main()


