
from python_nbt import nbt
import unittest

class InterfaceTest(unittest.TestCase):

    tag = nbt.NBTTagCompound()

    def test_setter(self):
        self.tag.setTagByte('byte', 8)
        self.assertEqual(self.tag['byte'].value, 8)


unittest.main()
