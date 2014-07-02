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

"""
Provide parsing and rooting around with tailoring2 project config files.

A config file is currently an ini file format, with one important section,
containing four important values::

    [project]
    messages = <paths>
    testcases = <paths>
    dictionary = <path>
    customization = <path>

where <paths> are colon-separated paths to files relative to the project root,
with possible java-style globs (* and ** are supported), and <path> is a single
path to a file relative to the project root.

Currently, the only way to handle this is by using the class-method:
``Configuration.from_file(filename, projectroot)``
"""

from ConfigParser import ConfigParser
import glob
import os

SECTION_NAME = 'project'
MESSAGE_KEY = 'messages'
TESTCASE_KEY = 'testcases'
DICTIONARY_KEY = 'dictionary'
CUSTOMIZATION_KEY = 'customization'

DEFAULT_CONFIG_FILE_NAME = 'project.cfg'


def expand_deep_path(globbedpath):
    basepath = globbedpath[:globbedpath.index("/**") + 1]
    walk = os.walk
    join = os.path.join
    return (join(base, filename) for base, _, files in walk(basepath)
        for filename in files)


def expand_path(globbedpath):
    if globbedpath.find('/**') >= 0:
        return expand_deep_path(globbedpath)
    return glob.iglob(globbedpath)


class Configuration(object):
    
    def __init__(self):
        self.messagepaths = []
        self.messagetree = {}
        self.testcasepaths = []
        self.testcasetree = {}
        self.dictionarypath = ''
        self.customizationpath = ''
        self.projectroot = ''
    
    @classmethod
    def from_file(cls, filename, projectdir=None):
        assert os.path.isfile(filename), filename
        
        originaldir = os.getcwd()
        targetdir = os.path.abspath(os.path.dirname(filename))
        projectdir = projectdir if projectdir is not None else targetdir
        
        config = cls()
        result = ConfigParser()
        result.read(filename)
        
        messages = result.get(SECTION_NAME, MESSAGE_KEY)
        testcases = result.get(SECTION_NAME, TESTCASE_KEY)
        dictionary = result.get(SECTION_NAME, DICTIONARY_KEY)
        customization = result.get(SECTION_NAME, CUSTOMIZATION_KEY)
        
        join = os.path.join
        
        def file_finder(locs, extension):
            headerlen = len(projectdir) + 1
            return (path[headerlen:] for messagepath in locs
                         for path in expand_path(join(projectdir, messagepath))
                         if path.endswith(extension))
        
        config.messagepaths.extend(
            file_finder(messages.split(':'), '.messages'))
        config.testcasepaths.extend(
            file_finder(testcases.split(':'), '.testcase'))        
        config.dictionarypath = join(projectdir, dictionary)
        config.customizationpath = join(projectdir, customization)
        config.projectroot = projectdir
        
        def makextree(fileext):
            return lambda x, y: x.setdefault(y,
                y if y.endswith(fileext) else dict())
        for path in config.messagepaths:
            reduce(makextree('.messages'), path.split('/'), config.messagetree)
        for path in config.testcasepaths:
            reduce(makextree('.testcase'),
                path.split('/'), config.testcasetree)
        
        os.chdir(originaldir)
        return config
