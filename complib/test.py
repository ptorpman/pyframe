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

from common.component import ComponentBase
from common.exceptions import NoReferencesException
from interfaces.iunknown      import IUnknown
from interfaces.iclassfactory import IClassFactory
from interfaces.iconfig       import IConfig


class TestFactory(ComponentBase, IClassFactory):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance                   = super(TestFactory, cls).__new__(cls, *args, **kwargs)
            cls._instance.name              = "TestFactory"
            cls._instance._created_instances = {}
            return cls._instance

        return cls._instance

    def __init__(self):
        super(TestFactory, self).__init__('TestFactory', 
                                          [IClassFactory.IID_IClassFactory()])

    # IClassFactory methods
    def CreateInstance(self, iid, name): 
        # FIXME: Check IID!
        if not self._created_instances.has_key(name):
            self._created_instances[name] = Test(name)
            return self._created_instances[name]

        raise Exception('Instance %s already exists' % name)

    def LockServer(self, block): 
        pass

class ITest(IUnknown):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def IID_ITest(cls): return UUID('{10000000-0000-0000-C000-000000000046}')
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abc.abstractmethod
    def test_me(self): pass



class Test(ComponentBase, ITest, IConfig):

    ProgID = 'test.Test.1'

    @classmethod
    def CLSID_Test(cls): return UUID('{a70f9a02-699e-11e4-96dd-0800277e7e72}')

    def __init__(self, name):
        ''' Constructor '''
        # Supported interfaces
        interfaces = [ITest.IID_ITest(), IConfig.IID_IConfig()]
        
        super(Test, self).__init__(name, interfaces)
        self._config = {}
        
    # ITest methods    
    def test_me(self):
        print '%s: Test me!' % self

    # IConfig methods
    def Configure(self, config):
        ''' Configure component '''
        self._config = config
        print 'DEBUG: %s: Loaded config - %s' % (self.name, self._config)
        

        

#--------------------------------------------------------------------
# COMPONENT REGISTRATION METHODS
#--------------------------------------------------------------------

def load_this():
    ''' To be called by CompLoader '''

    print 'DEBUG: Loading file... %s' % __file__
    from system.registrar import Registrar
    Registrar().CoRegisterClassObject(Test.CLSID_Test(), Test.ProgID, TestFactory())
