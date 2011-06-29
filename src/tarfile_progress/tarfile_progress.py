'''
Created on 29 Jun 2011

@author: Thomas Purchas
'''
import tarfile
import os

class TarFile(tarfile.TarFile):
    '''
    classdocs
    '''
    def __init__(self, name=None, mode="r", fileobj=None, format=None,
        tarinfo=None, dereference=None, ignore_zeros=None, encoding=None,
        errors=None, pax_headers=None, debug=None, errorlevel=None):
        '''
        Open an (uncompressed) tar archive `name'. `mode' is either 'r' to
        read from an existing archive, 'a' to append data to an existing
        file or 'w' to create a new file overwriting an existing one. `mode'
        defaults to 'r'.
        If `fileobj' is given, it is used for reading or writing data. If it
        can be determined, `mode' is overridden by `fileobj's mode.
        `fileobj' is not closed, when TarFile is closed.
        '''
        
        self.__progresscallback = None
        
        tarfile.TarFile.__init__(self, name, mode, fileobj, format,
                                 tarinfo, dereference, ignore_zeros, encoding,
                                 errors, pax_headers, debug, errorlevel)
        
    def add(self, name, arcname=None, recursive=True, exclude=None, filter=None, progress=None):
        '''
        Add the file *name* to the archive. *name* may be any type of file (directory,
        fifo, symbolic link, etc.). If given, *arcname* specifies an alternative name
        for the file in the archive. Directories are added recursively by default. This
        can be avoided by setting *recursive* to :const:`False`. If *exclude* is given
        it must be a function that takes one filename argument and returns a boolean
        value. Depending on this value the respective file is either excluded
        (:const:`True`) or added (:const:`False`). If *filter* is specified it must
        be a function that takes a :class:`TarInfo` object argument and returns the
        changed :class:`TarInfo` object. If it instead returns :const:`None` the :class:`TarInfo`
        object will be excluded from the archive. See :ref:`tar-examples` for an
        example.
        
        *progress* will be called with a signal integer with a value between 0 and 100,
        which represents the percentage of the file that has been added. It is
        guarrentied that the passed value will only increase.
        
        ..  versionchanged:: 2.6
            Added the *exclude* parameter.
        
        ..  versionchanged:: 2.7
            Added the *filter* parameter.
        
        ..  deprecated:: 2.7
            The *exclude* parameter is deprecated, please use the *filter* parameter
            instead.  For maximum portability, *filter* should be used as a keyword
            argument rather than as a positional argument so that code won't be
            affected when *exclude* is ultimately removed.
        '''
        
        if progress is not None:
            progress(0)
            self.__progresscallback = progress
            
        return tarfile.TarFile.add(self, name, arcname, recursive, exclude, filter)
        
    def addfile(self, tarinfo, fileobj=None):
        """
        Add the TarInfo object `tarinfo' to the archive. If `fileobj' is
        given, tarinfo.size bytes are read from it and added to the archive.
        You can create TarInfo objects using gettarinfo().
        On Windows platforms, `fileobj' should always be opened with mode
        'rb' to avoid irritation about the file size.
        """
        print 'addfile'
        if fileobj is not None:
            
            fileobj = filewrapper(fileobj, self.__progresscallback)
   
        return tarfile.TarFile.addfile(self, tarinfo, fileobj)
            
class filewrapper(object):
    '''
    This is a wrapper for a file object. I uses the __getattr__ function to cheat.
    '''
    
    def __init__(self, fileobj, progress):
        self._fileobj = fileobj
        
        # Get the file length
        currentpos = fileobj.tell()
        
        fileobj.seek(0, os.SEEK_END)
        
        self._length = fileobj.tell()
        
        fileobj.seek(currentpos, os.SEEK_SET)
        
        if progress is not None:
            progress(0)
        self._progress = progress
        self._lastprogress = 0
        
        
    def read(self, size = -1):
        data = self._fileobj.read(size)
        
        if self._progress is not None:
            progress = self._fileobj.tell()
            
            progress = (progress * 100) / self._length
            
            if progress > self._lastprogress:
                self._progress(progress)
        
        return data
        
    def __getattr__(self, name):
        return getattr(self._fileobj, name)
    

open = TarFile.open