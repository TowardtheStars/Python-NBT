import python_nbt.nbt as nbt
from gzip import GzipFile
import json

file = nbt.read_from_nbt_file("./test/file.nbt")

print(json.dumps(file.json_obj, indent=2))
