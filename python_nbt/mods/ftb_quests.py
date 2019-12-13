
from .. import nbt
from enum import Enum

class QuestShape(Enum):
    DEFAULT = "default"
    CIRCLE = "circle"
    SQUARE = "square"
    DIAMOND = "diamond"
    RSQUARE = "rsquare"
    PENTAGON = "pentagon"
    HEXAGON = "hexagon"
    HEART = "heart"
    GEAR = "gear"

class QuestObjBase:
    TITLE = 'title'

    def __init__(self):
        self.id = 0
        self.invalid = False
        self.tags = set()
        self.data = None

    @property
    def title(self):
        return self.data.get(self.TITLE)

    @title.setter
    def title(self, v):
        self.data[self.TITLE] = nbt.NBTTagString(v)

    

class Chapter(QuestObjBase):
    ALWAYS_INVISIBLE = "always_invisible"
    DEFAULT_QUEST_SHAPE = "default_quest_shape"

    def __init__(self, file=None):
        self.data = nbt.NBTTagCompound(os.path.join(file, "chapter.nbt"))
        self.quests = self.load_quests(file)
    
    @property
    def alwaysVisible(self):
        return self.data.get(self.ALWAYS_INVISIBLE, False)

    @alwaysVisible.setter
    def alwaysVisible(self, v:bool):
        self.data[self.ALWAYS_INVISIBLE] = nbt.NBTTagByte(1 if v else 0)
    
    @property
    def default_quest_shape(self):
        return self.data.get(self.DEFAULT_QUEST_SHAPE, Shape.DEFAULT)

    @default_quest_shape.setter
    def default_quest_shape(self, v):
        if not isinstance(v, str) or v not in dir(QuestShape) or v.starswith("__"):
            raise ValueError("Must an element from Shape!")
        self.data[self.DEFAULT_QUEST_SHAPE] = nbt.NBTTagString(v)

