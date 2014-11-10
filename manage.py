"""
import imp
try:
    imp.find_module('myselector.settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)
"""



"""
#!/usr/bin/env python
from django.core.management.base import execute_manager

#import seed project settings
from mydata4 import settings
#from mydata6 import settings

if __name__ == "__main__":
    execute_manager(settings)

"""

#django 1.5 version of manage.py

#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydatademo.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


