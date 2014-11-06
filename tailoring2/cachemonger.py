# COPYRIGHT (c) 2008
# THE REGENTS OF THE UNIVERSITY OF MICHIGAN
# ALL RIGHTS RESERVED
#  
# PERMISSION IS GRANTED TO USE, COPY, CREATE DERIVATIVE WORKS AND
# REDISTRIBUTE THIS SOFTWARE AND SUCH DERIVATIVE WORKS FOR NONCOMMERCIAL
# EDUCATION AND RESEARCH PURPOSES, SO LONG AS NO FEE IS CHARGED, AND SO
# LONG AS THE COPYRIGHT NOTICE ABOVE, THIS GRANT OF PERMISSION, AND THE
# DISCLAIMER BELOW APPEAR IN ALL COPIES MADE; AND SO LONG AS THE NAME OF
# THE UNIVERSITY OF MICHIGAN IS NOT USED IN ANY ADVERTISING OR PUBLICITY
# PERTAINING TO THE USE OR DISTRIBUTION OF THIS SOFTWARE WITHOUT SPECIFIC,
# WRITTEN PRIOR AUTHORIZATION.
#  
# THIS SOFTWARE IS PROVIDED AS IS, WITHOUT REPRESENTATION FROM THE
# UNIVERSITY OF MICHIGAN AS TO ITS FITNESS FOR ANY PURPOSE, AND WITHOUT
# WARRANTY BY THE UNIVERSITY OF MICHIGAN OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE REGENTS OF THE
# UNIVERSITY OF MICHIGAN SHALL NOT BE LIABLE FOR ANY DAMAGES, INCLUDING
# SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, WITH RESPECT TO
# ANY CLAIM ARISING OUT OF OR IN CONNECTION WITH THE USE OF THE SOFTWARE,
# EVEN IF IT HAS BEEN OR IS HEREAFTER ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGES.

"""Cache file-based serialized objects in memory. Update cache based on
file's modification time.
"""

import os
import os.path


def mtime(filepath):
    """return mtime of given file. Convenience to make call more like path.py's call"""
    return os.stat(filepath).st_mtime
    

class FilepathCache(object):
    """caches file-based serialized objects (like a list of tailoring commands) in memory.
    updates cache based on file's modification time.
    """
    
    def __init__(self):
        self.items = {}  # key = path, val = (const-date, obj) tuple

    def clear(self):
        self.items = {}

    def _make_new_entry(self, filepath, ctorfunc):
        """(time-long, obj) tuple"""
        return (mtime(filepath), ctorfunc(filepath))
        
    def get(self, filepath, ctorfunc):
        """get object from filepath...
            - installing in cache if necessary
            - reinstalling in cache if cache is out of date

        ctorfunc is a constructor function that takes a filepath. it
        will be called to create the cached object when the filepath
        isn't in the cache or the file mod time is out of date.
        """
        if not filepath in self.items:
            self.items[filepath] = self._make_new_entry(filepath, ctorfunc)
        else:
             # check for out-of-date
            file_mtime, obj = self.items[filepath]
            if mtime(filepath) > file_mtime:
                # too old, reconstruct
                self.items[filepath] = self._make_new_entry(filepath, ctorfunc)
        # return object part of entry
        return self.items[filepath][1]
