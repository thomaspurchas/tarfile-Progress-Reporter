==========================
tarfile Progress Extension
==========================

This module is a wrapper around the
standard tarfile libary in Python. It 
adds the ability to pass a progress 
callback to the following ```TarFile```
methods:

*   ```TarFile.add()```
*   ```TarFile.addfile()```
*   ```TarFile.extractall()```
*   ```TarFile.extract()```
*   ```TarFile.extractfile()```

Each of those methods has a new ```progress```
argument. Any function passed to the
```progress``` argument will be called once
per percentage increace, with a single integer
value between 0 and 100.

This module is a drop-in replacement for the 
standard tarfile libary, and should only require
the ```import``` statments be changes.

Examples:
=========

Replacing ```tarfile``` with ```tarfile_progress```
---------------------------------------------------

Replace the following:

```python
import tarfile
```
with
```python
from tarfile_progress import tarfile_progress as tarfile
```

Setting up a callback
---------------------

This uses the included example function.

```python
dsafs```
