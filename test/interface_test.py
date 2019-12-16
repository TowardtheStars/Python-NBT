
from python_nbt import nbt
import unittest

class InterfaceTest(unittest.TestCase):

    tag = nbt.NBTTagCompound()

    def test01_setter(self):
        self.tag.setTagByte('byte', 8)
        self.tag.setTagShort('short', 32767)
        self.tag.setTagInt('int', 16777216)
        self.tag.setTagLong('long', -8000000000000)
        self.tag.setTagString('string', 'test')
        self.tag.setTagByteArray('byte_array', [1,2,3])
        self.tag.setTagIntArray('int_array', [400, 500, 600])
        self.tag.setTagLongArray('long_array', [606664, 46164546])

        self.assertEqual(self.tag.getTagByte('byte'), 8)
        self.assertEqual(self.tag.getTagShort('short'), 32767)
        self.assertEqual(self.tag.getTagInt('int'), 16777216)
        self.assertEqual(self.tag.getTagLong('long'), -8000000000000)
        self.assertEqual(self.tag.getTagString('string'), 'test')
        self.assertEqual(self.tag.getTagByteArray('byte_array'), [1,2,3])
        self.assertEqual(self.tag.getTagIntArray('int_array'), [400, 500, 600])
        self.assertEqual(self.tag.getTagLongArray('long_array'), [606664, 46164546])


unittest.main()
