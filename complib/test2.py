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

#--------------------------------------------------------------------
# COMPONENT CLASSES 
#--------------------------------------------------------------------
import abc
import json
from uuid import UUID

from common.component         import ComponentBase
from common.exceptions        import NoReferencesException
from interfaces.iunknown      import IUnknown
from interfaces.iclassfactory import IClassFactory
from interfaces.iconfig       import IConfig
from system.trace             import Trace
from complib.itest            import ITest

class Test2Factory(ComponentBase, IClassFactory):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance                   = super(Test2Factory, cls).__new__(cls, *args, **kwargs)
            cls._instance.name              = "Test2Factory"
            cls._instance._created_instances = {}
            return cls._instance

        return cls._instance

    def __init__(self):
        super(Test2Factory, self).__init__('Test2Factory', 
                                          [IClassFactory.IID_IClassFactory()])

    # IClassFactory methods
    def CreateInstance(self, iid, name): 
        # FIXME: Check IID!
        if not self._created_instances.has_key(name):
            self._created_instances[name] = Test2(name)
            return self._created_instances[name]

        raise Exception('Instance %s already exists' % name)

    def LockServer(self, block): 
        pass

class Test2(ComponentBase, ITest, IConfig):

    ProgID = 'test.Test2.1'

    @classmethod
    def CLSID(cls): return UUID('{a70f9a02-699e-11e4-96dd-0800277e7e80}')

    def __init__(self, name):
        ''' Constructor '''
        # Supported interfaces
        interfaces = [ITest.IID_ITest(), IConfig.IID_IConfig()]
        
        super(Test2, self).__init__(name, interfaces)
        self._config = {}
        
    # ITest methods    
    def test_me(self):
        Trace().debug('%s: Test me!' % self)
        
    # IConfig methods
    def Configure(self, config):
        ''' Configure component '''
        self._config = config
        Trace().debug('%s: Loaded config - %s' % (self.name, self._config))
        

#--------------------------------------------------------------------
# COMPONENT REGISTRATION METHODS
#--------------------------------------------------------------------

def load_this():
    ''' To be called by CompLoader '''
    from system.registrar import Registrar
    Registrar().CoRegisterClassObject(Test2.CLSID(), Test2.ProgID, Test2Factory())
