from struct import Struct, error as StructError
from gzip import GzipFile

from . import _util

TAG_END         =  0
TAG_BYTE        =  1
TAG_SHORT       =  2
TAG_INT         =  3
TAG_LONG        =  4
TAG_FLOAT       =  5
TAG_DOUBLE      =  6
TAG_BYTE_ARRAY  =  7
TAG_STRING      =  8
TAG_LIST        =  9
TAG_COMPOUND    = 10
TAG_INT_ARRAY   = 11
TAG_LONG_ARRAY  = 12

class NBTTagBase:

    _type_id = None

    def __init__(self, value=None, buffer=None):
        """
        Don't use this
        This is just for code reuse
        """
        self._value = value
        if buffer:
            self._read_buffer(buffer)

    def _write_buffer(self, buffer):
        pass

    def _read_buffer(self, buffer):
        pass

    @property
    def type_id(self):
        return self._type_id

    @property
    def value(self):
        return self._value

    def _value_json_obj(self):
        return self.value

    @property
    def json_obj(self):
        """
        Return json format object of this NBT tag.
        """
        return {"type_id":self.type_id, "value": self._value_json_obj()}

    def __str__(self):
        return str(self.json_obj)

    def __repr__(self):
        return self.json_obj.__repr__()


class NBTTagEnd(NBTTagBase):
    """
    This is just for File I/O
    """
    
    _type_id = TAG_END
    fmt = Struct(">b")

    def __init__(self):
        super().__init__()

    def _read_buffer(self, buffer):
        value = self.fmt.unpack(buffer.read(1))[0]
        if value != 0:
            raise ValueError(
                "A Tag End must be rendered as '0', not as '%d'." % value
            )

    def _write_buffer(self, buffer):
        buffer.write(b'\x00')


class NBTTagSingleValue(NBTTagBase):
    """
    Just for code reuse
    """

    fmt = None

    def __init__(self, value=None, buffer=None):
        super().__init__(value=value, buffer=buffer)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if not self._validate(v):
            raise ValueError("Cannot apply value %s to %s" % (v, self.__class__.__name__))
        self._value = v

    def _validate(self, v):
        return True

    def _read_buffer(self, buffer):
        self.value = self.fmt.unpack(buffer.read(self.fmt.size))[0]

    def _write_buffer(self, buffer):
        buffer.write(self.fmt.pack(self.value))

    def _value_json_obj(self):
        return self.value


class NBTTagContainerList(NBTTagBase, _util.RestrictedList):
    """
    Just for code reuse and better interfaces
    """
    
    def __init__(self, validator, buffer=None):
        _util.RestrictedList.__init__(self, validator=validator)
        if buffer:
            self._read_buffer(buffer)

    @property
    def value(self):
        return self[:]

    def _value_json_obj(self):
        return self[:]


# == Actual NBT tag types from here ==

class NBTTagByte(NBTTagSingleValue):

    _type_id = TAG_BYTE
    fmt = Struct(">b")
    
    def __init__(self, value=0, buffer=None):
        super().__init__(value=value, buffer=buffer)
    
    def _validate(self, v):
        return isinstance(v, int) and v in range(-0x80, 0x80)


class NBTTagShort(NBTTagSingleValue):

    _type_id = TAG_SHORT
    fmt = Struct(">h")

    def __init__(self, value=0, buffer=None):
        super().__init__(value=value, buffer=buffer)

    def _validate(self, v):
        return isinstance(v, int) and v in range(-0x8000, 0x8000)


class NBTTagInt(NBTTagSingleValue):

    _type_id = TAG_INT
    fmt = Struct(">i")

    def __init__(self, value=0, buffer=None):
        super().__init__(value=value, buffer=buffer)

    def _validate(self, v):
        return isinstance(v, int) and v in range(-0x80000000, 0x80000000)


class NBTTagLong(NBTTagSingleValue):

    _type_id = TAG_LONG
    fmt = Struct(">q")

    def __init__(self, value=0, buffer=None):
        super().__init__(value=value, buffer=buffer)

    def _validate(self, v):
        return isinstance(v, int) and v in range(-0x8000000000000000, 0x8000000000000000)


class NBTTagFloat(NBTTagSingleValue):

    _type_id = TAG_FLOAT
    fmt = Struct(">f")

    def __init__(self, value=.0, buffer=None):
        super().__init__(value=value, buffer=buffer)

    def _validate(self, v):
        return isinstance(v, float)


class NBTTagDouble(NBTTagSingleValue):

    _type_id = TAG_FLOAT
    fmt = Struct(">d")

    def __init__(self, value=.0, buffer=None):
        super().__init__(value=value, buffer=buffer)

    def _validate(self, v):
        return isinstance(v, float)


class NBTTagString(NBTTagSingleValue):

    _type_id = TAG_STRING

    def __init__(self, value="", buffer=None):
        super().__init__(value=value, buffer=buffer)

    def _validate(self, v):
        return isinstance(v, str) and len(self.value) < 0x8000

    def _read_buffer(self, buffer):
        length = NBTTagShort(buffer=buffer).value
        s = buffer.read(length)
        if len(s) != length:
            raise StructError()
        self.value = s.decode("utf-8")

    def _write_buffer(self, buffer):
        byte_code = self.value.encode("utf-8")
        length = NBTTagShort(len(byte_code))
        length._write_buffer(buffer)
        buffer.write(byte_code)


class NBTTagCompound(NBTTagBase, _util.TypeRestrictedDict):

    _type_id = TAG_COMPOUND
    
    def __init__(self, buffer=None):
        _util.TypeRestrictedDict.__init__(self, value_types=NBTTagBase, key_types=str)
        if buffer:
            self._read_buffer(buffer)

    def _read_buffer(self, buffer):
        while True:
            _type = NBTTagByte(buffer=buffer).value
            if _type == TAG_END:
                break
            else:
                name = NBTTagString(buffer=buffer).value
                if not _type in TAGLIST.keys():
                    raise ValueError("Unrecognised tag type %d" % _type)
                tag = TAGLIST[_type](buffer=buffer)
                self[name] = tag

    def _write_buffer(self, buffer):
        for key, tag in self.items():
            NBTTagByte(value=tag.type_id)._write_buffer(buffer)
            NBTTagString(value=key)._write_buffer(buffer)
            tag._write_buffer(buffer)
        NBTTagEnd()._write_buffer(buffer)

    def _value_json_obj(self):
        result = {}
        for key, value in self.items():
            result[key] = value.json_obj
        return result


class NBTTagByteArray(NBTTagContainerList):

    _type_id = TAG_BYTE_ARRAY

    def __init__(self, buffer=None):
        super().__init__(
            validator=lambda v: isinstance(v, int) and v in range(-0x80, 0x80),
            buffer=buffer
        )
    
    def _read_buffer(self, buffer):
        length = NBTTagInt(buffer=buffer).value
        self.clear()
        self.extend(list(bytearray(buffer.read(length))))

    def _write_buffer(self, buffer):
        length = NBTTagInt(len(self.value))
        length._write_buffer(buffer)
        buffer.write(bytes(self.value))


class NBTTagIntArray(NBTTagContainerList):

    _type_id = TAG_INT_ARRAY

    def __init__(self, buffer=None):
        super().__init__(
            validator=lambda v: isinstance(v, int) and v in range(-0x80000000, 0x80000000),
            buffer=buffer
        )

    def _read_buffer(self, buffer):
        length = NBTTagInt(buffer=buffer).value
        fmt = Struct(">" + str(length) + "i")
        self.clear()
        self.extend(list(fmt.unpack(buffer.read(fmt.size))))

    def _write_buffer(self, buffer):
        length = len(self.value)
        fmt = Struct(">" + str(length) + "i")
        NBTTagInt(length)._write_buffer(buffer)
        buffer.write(fmt.pack(*self.value))


class NBTTagLongArray(NBTTagContainerList):

    _type_id = TAG_LONG_ARRAY

    def __init__(self, buffer=None):
        super().__init__(
            validator=lambda v: isinstance(v, int) and v in range(-0x8000000000000000, 0x8000000000000000),
            buffer=buffer
        )

    def _read_buffer(self, buffer):
        length = NBTTagInt(buffer=buffer).value
        fmt = Struct(">" + str(length) + "q")
        self.clear()
        self.extend(list(fmt.unpack(buffer.read(fmt.size))))

    def _write_buffer(self, buffer):
        length = len(self.value)
        fmt = Struct(">" + str(length) + "q")
        NBTTagInt(length)._write_buffer(buffer)
        buffer.write(fmt.pack(*self.value))


class NBTTagList(NBTTagContainerList):

    _type_id = TAG_LIST

    def __init__(self, tag_type=None, buffer=None):
        """
        If you are creating a NBTTagList ypurself,
        Please specify a tag_type (must be a subclass of NBTTagBase)
        """

        if tag_type:
            self._tag_type_id = tag_type.type_id
        else:
            self._tag_type_id = None
        super().__init__(
            validator=lambda v: isinstance(v, self.tag_type),
            buffer=buffer
        )

    @property
    def tag_type_id(self):
        return self._tag_type_id

    @property
    def tag_type(self):
        return TAGLIST[self._tag_type_id]

    def _read_buffer(self, buffer):
        self._tag_type_id = NBTTagByte(buffer=buffer).value
        self.clear()
        length = NBTTagInt(buffer=buffer).value
        for i in range(length):
            self.append(TAGLIST[self._tag_type_id](buffer=buffer))

    def _write_buffer(self, buffer):
        if self.tag_type_id == None:
            raise ValueError("No type specified for list: %s" % (self.name))
        NBTTagByte(self.tag_type_id)._write_buffer(buffer)
        length = NBTTagInt(len(self))
        length._write_buffer(buffer)
        for i, tag in enumerate(self.value):
            if tag.type_id != self.type_id:
                raise ValueError(
                    "List element %d(%s) has type %d != container type %d" %
                    (i, tag, tag.idx, self.tagID))
            tag._write_buffer(buffer)

    def _value_json_obj(self):
        return [tag._value_json_obj() for tag in self.value]


TAGLIST = {
    TAG_END         : NBTTagEnd, 
    TAG_BYTE        : NBTTagByte, 
    TAG_SHORT       : NBTTagShort,
    TAG_INT         : NBTTagInt, 
    TAG_LONG        : NBTTagLong, 
    TAG_FLOAT       : NBTTagFloat,
    TAG_DOUBLE      : NBTTagDouble, 
    TAG_BYTE_ARRAY  : NBTTagByteArray,
    TAG_STRING      : NBTTagString, 
    TAG_LIST        : NBTTagList,
    TAG_COMPOUND    : NBTTagCompound,
    TAG_INT_ARRAY   : NBTTagIntArray,
    TAG_LONG_ARRAY  : NBTTagLongArray
}


# Map Minecraft Wiki names to class names
# For compatibility
TAG            = NBTTagBase
TAG_Byte       = NBTTagByte
TAG_Short      = NBTTagShort
TAG_Int        = NBTTagInt
TAG_Long       = NBTTagLong
TAG_Float      = NBTTagFloat
TAG_Double     = NBTTagDouble
TAG_Byte_Array = NBTTagByteArray
TAG_Int_Array  = NBTTagIntArray
TAG_Long_Array = NBTTagLongArray
TAG_String     = NBTTagString
TAG_List       = NBTTagList
TAG_Compound   = NBTTagCompound
TAG_End        = NBTTagEnd

def read_from_nbt_file(file):
    """
    Read NBTTagCompound from a NBT file
    """
    _file = GzipFile(file, "rb") if isinstance(file, str) else GzipFile(fileobj=file, mode="rb")
    _type = NBTTagByte(buffer=_file).value
    _name = NBTTagString(buffer=_file).value
    return TAGLIST[_type](buffer=_file)

def write_to_nbt_file(file, tag:NBTTagCompound, name=''):
    """
    Write a NBTTagCompound to a NBT file
    name affects nothing currently
    """
    _file = GzipFile(file, "wb") if isinstance(file, str) else GzipFile(fileobj=file, mode="wb")
    NBTTagByte(tag.type_id)._write_buffer(_file)
    NBTTagString(name)._write_buffer(_file)
    tag._write_buffer(_file)

