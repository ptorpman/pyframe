# -*- mode: Python; fill-column: 75; comment-column: 70; -*-
#
#  This file is part of Torpman's PyFrame 
#         https://github.com/ptorpman/pyframe
# 
#  This sofware is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
# 
#  This software is distributed in the hope that it will 
#  be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.or/licenses/>.
#
#  Author: Peter R. Torpman (peter at torpman dot se)
#
#------------------------------------------------------------------------------
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
