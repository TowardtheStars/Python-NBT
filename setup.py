from setuptools import setup
from python_nbt import VERSION

setup(
  name             = 'Python-NBT',
  version          = ".".join(str(x) for x in VERSION),
  description      = 'Named Binary Tag Reader/Writer',
  author           = 'Thomas Woolford',
  author_email     = 'woolford.thomas@gmail.com',
  url              = 'http://github.com/twoolie/NBT',
  license          = open("LICENSE.txt").read(),
  long_description = open("README.txt").read(),
  packages         = ['nbt'],
  classifiers      = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
  ]
)
