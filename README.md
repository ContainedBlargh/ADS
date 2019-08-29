# ADS - Assignment Distribution Script

A simple python script for distributing assignments between TAs.

## Usage

```
usage: ads.py [-h] [-z] path destination name [name ...]

Downloads and distributes assignment submissions to teaching assistents.

positional arguments:
  path         The path to the assignment zip.
  destination  The path to a folder that will be made by this process and
               filled with the assignments
  name         The names of the TAs (ie. "jvoi, khjo")

optional arguments:
  -h, --help   show this help message and exit
  -z           If set, the resulting folder is zipped as well.
```

## Requirements

* Python 3 or newer
