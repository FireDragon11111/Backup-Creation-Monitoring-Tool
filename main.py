import os
import sys
import atexit
from gui import create_gui, cleanup
import license

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    
    license.create_license_file()
    
    atexit.register(cleanup)
    create_gui()
