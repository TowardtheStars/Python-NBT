
from .. import nbt

class ItemStack():
    """
    ~1.12.2
    """
    def __init__(self, registry_name="minecraft:air", damage=0, count=1, tag=None):
        self.registry_name = registry_name
        self.damage = damage
        self.tag = tag or nbt.NBTTagCompound()
        self.count = count