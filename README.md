# tarfile Progress Extension #

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

## Notes ##

When you use the ```TarFile.add()``` method your
callback will receive a percentage complete for
each file as it is added, rather than for the
entire operation.

This means that when displaying information to
users you need make it clear the the progress
bar will fill up multiple times, once for each
file added.

This also applies to the ```TarFile.extractall()```
method, if the input tar file is a stream. If the
input tar file is a bog standard file then your
callback will receive a percentage complete for
the entire operation.

## Examples ##

### Replacing ```tarfile``` with ```tarfile_progress``` ###

Replace the following:

```python
import tarfile
```
with

```python
from tarfile_progress import tarfile_progress as tarfile
```

### From the command line ###

This example uses the included example function, and is
done from the command line. (Additional whitespace has been added)

```
>>> from tarfile_progress import tarfile_progress as tarfile
>>> tar = tarfile.open('test.tar', 'w')
>>> tar.add('monty', progress = tarfile.progressprint)
|##################################################| 100% File complete
>>> tar.extractall(tarfile.progressprint)
|##################################################| 100% File complete
```

### Setting up a callback ###

This uses the included example function.

```python
from tarfile_progress import tarfile_progress as tarfile

print 'Opening a new file'

# Open up a new tar file for writing
tar = tarfile.open('test.tar', 'w')

print 'Adding a new file'

# Add a new file to it, and pass it the progress callback
tar.add('monty', progress = tarfile.progressprint)

print 'Extracting files'

# Extract all the files, with progress
tar.extractall(progress = tarfile.progressprint)
```
This will result in the following output

```
Opening a new file
Adding a new file
|##################################################| 100% File complete
Extracting files
|##################################################| 100% File complete
```