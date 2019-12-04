from setuptools import setup
from python_nbt import VERSION

setup(
  name             = 'Python-NBT',
  version          = ".".join(str(x) for x in VERSION),
  description      = 'NBT Reader/Writer',
  author           = 'TowardtheStars',
  author_email     = 'hty16@mail.ustc.edu.cn',
  url              = 'https://github.com/TowardtheStars/Python-NBT',
  license          = open("LICENSE").read(),
  long_description = open("README.txt").read(),
  packages         = ['python_nbt'],
  classifiers      = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
  ]
)
