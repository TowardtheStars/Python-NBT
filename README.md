# Python-NBT

A python library for reading and writing NBT files. Compatible with json.

Based on NBT Version: 19133 (Current version used by Minecraft)

## What is NBT

> NBT (Named Binary Tag) is a tag based binary format designed to carry large amounts of binary data with smaller amounts of additional data. An NBT file consists of a single GZIPped Named Tag of type TAG_Compound.

From official [Minecraft Wiki](https://minecraft.gamepedia.com/NBT_format).

## Installation

```bash
pip install Python-NBT
```

## Usage

### Read an NBT file

```Python
>>> import python_nbt.nbt as nbt
>>> file = nbt.read_from_nbt_file("file.nbt")
```

This function returns an instance of NBTTagCompound, or by the name on Minecraft Wiki, an instance of TAG_Compound. It only accept 1 argument, which can be either a file path string or an opened file stream.

The TAG_Compound acts like a `dict` in Python. More accurately, it is a subclass of `dict` in Python with some restrictions put on its keys and values. So you can get, and set its items as shown below:

```Python
>>> file['drop_loot_crates']
{'type_id': 1, 'value': 0}
>>> file['drop_loot_crates'] = nbt.TAG_Byte(1)
>>> file['drop_loot_crates']
{'type_id': 1, 'value': 1}
```

In the dict shown as above, the key `'type_id'` represents the type id of an NBT. In our example, its `'type_id'` is `1`, which indicates this NBT is a TAG_Byte. And `'value'` indicates its actual value.

### Write an NBT file

Once you've completed editing an NBT, you can store it into an NBT file with the function below:

```Python
write_to_nbt_file(file, tag)
```

The first argument `file` should be a path string or a file stream to the file you want to create/write. The second argument `tag` is the NBT you want to write.

### Compat with Json

If you want to export NBT in json, you can use `NBTTagBase.json_obj(full_json=True)` to get an json style `dict` that contains all the NBT information.
After that, you can use `json` module in Python to do whatever you want.
If you want a simpler version, which omits type id of an NBT and NBTs inside it, set `full_json` to `False`.
**Note**: Changing `full_json` to `False` will also turn json dict of nested tags into simple version.

If you want to import NBT from a json object, you can use `nbt.from_json(json_obj)` to do so.
This function will return an NBT object. And its argument must be as same format as what `NBTTagBase.json_obj(full_json=True)` exports.

## Future features

Ticked entries are finished.

- [x] More json compat
  - [x] Convert json into NBT
  - [x] Better and configurable json output (omitting NBT types)
- [ ] Convenient classes for reading and writing Minecraft saves files
  - [ ] World
  - [ ] Region
  - [ ] Chunk
  - [ ] ItemStack
  - [ ] TileEntity
  - [ ] Entity
  - [ ] Player
- [ ] Utilities for mods
  - [ ] [FTB Quests](https://github.com/FTBTeam/FTB-Quests) [(CurseForge Link)](https://www.curseforge.com/minecraft/mc-mods/ftb-quests)
  - [ ] [GameStages](https://github.com/Darkhax-Minecraft/Game-Stages) [(CurseForge Link)](https://minecraft.curseforge.com/projects/game-stages)
  - [ ] Recognize blocks and items form mods in World according to NEI exports
- [x] A detailed ~~doc/~~wiki
- [ ] More convenient interfaces for NBT (try to fully abandon `value` property, and makes everthing just it should be)
  - [ ] Operators for numeric tags
    - [ ] +, -, *, /
    - [ ] **, //
    - [ ] >, <
  - [x] List interfaces for array-like NBT
  - [x] Dict interfaces for dict-like NBT
