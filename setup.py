from setuptools import setup
from python_nbt import VERSION

with open("README.md", "r", encoding='utf-8') as file:
  long_description = file.read()

setup(
  name             = 'Python-NBT',
  version          = ".".join(str(x) for x in VERSION),
  description      = 'A python library for reading and writing NBT files',
  author           = 'TowardtheStars',
  author_email     = 'hty16@mail.ustc.edu.cn',
  url              = 'https://github.com/TowardtheStars/Python-NBT',
  license          = "GPLv3",
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages         = ['python_nbt'],
  classifiers      = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
  ]
)
