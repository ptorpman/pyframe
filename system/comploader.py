import glob
import imp
import os

class CompLoader(object):
    ''' The singleton that loads components in the component library into the system '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CompLoader, cls).__new__(cls, *args, **kwargs)
            return cls._instance

        return cls._instance

    def __init__(self):
        pass

    def load_components(self, directories):
        print '* Loading components from %s ...' % directories

        for d in directories:
            files = glob.glob('%s/*.py' % d)

            for f in files:
                mod_name,file_ext = os.path.splitext(os.path.split(f)[-1])
                py_mod = imp.load_source(mod_name, f)

                if hasattr(py_mod, 'load_this'):
                    py_mod.load_this()
