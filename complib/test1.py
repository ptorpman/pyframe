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
from interfaces.iconnect      import IConnect
from system.trace             import Trace
from complib.itest            import ITest
from interfaces.ischeduler    import ISchedulerClient, ISchedulerServer
from system.scheduler         import Scheduler


class Test1(ComponentBase, IConfig, IConnect, ISchedulerClient):
    '''  
    Component Example
    This component implements some basic interfaces to make it
    connectable and configurable.
    '''

    ProgID = 'test.Test1.1'

    @classmethod
    def CLSID(cls): return UUID('{a70f9a02-699e-11e4-96dd-0800277e7e72}')

    def __init__(self, name):
        ''' Constructor '''
        # Supported interfaces
        interfaces = [ IConfig.IID_IConfig(),
                       IConnect.IID_IConnect(),
                       ISchedulerClient.IID_ISchedulerClient() ]
        super(Test1, self).__init__(name, interfaces)
        self._config = {}
        self._connections = []
        self._scheduler = None
        
    # IConfig methods
    def Configure(self, config):
        ''' Configure component '''
        self._config = config
        Trace().logger().debug('%s: Loaded config - %s' % (self.name, self._config))

        self._scheduler = Scheduler().QueryInterface(ISchedulerServer.IID_ISchedulerServer())
        self._scheduler.AddScheduledComponent(self)
        
        
    # IConnect methods
    def Connect(self, instance, interface, args):
        ''' Connect to other components '''
        Trace().logger().debug('%s: Connect - %s %s %s' % (self.name, instance, interface, args))

        # Make sure other instance has the specified interface
        iface = instance.QueryInterface(interface)

        # Store connection information if needed later
        self._connections.append((iface, interface))

        # Execute interface method implemented by other instance
        iface.test_me(args)

    # ISchedulerClient methods
    def Execute(self, slice):
        print "%s: Executing slice... %d " % (self.name, slice)
        
        
#--------------------------------------------------------------------
# CLASS OBJECT (FACTORY)
#--------------------------------------------------------------------

class Test1Factory(ComponentBase, IClassFactory):
    ''' This class is a factory for creating Test1 instances '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance                   = super(Test1Factory, cls).__new__(cls, *args, **kwargs)
            cls._instance.name              = "Test1Factory"
            cls._instance._created_instances = {}
            return cls._instance

        return cls._instance

    def __init__(self):
        super(Test1Factory, self).__init__('Test1Factory', 
                                          [IClassFactory.IID_IClassFactory()])

    # IClassFactory methods
    def CreateInstance(self, iid, name): 
        # FIXME: Check IID!
        if not self._created_instances.has_key(name):
            self._created_instances[name] = Test1(name)
            return self._created_instances[name]

        raise Exception('Instance %s already exists' % name)

    def LockServer(self, block): 
        pass

    

#--------------------------------------------------------------------
# COMPONENT REGISTRATION METHODS
#--------------------------------------------------------------------

def load_this():
    ''' To be called by CompLoader '''
    from system.registrar import Registrar
    Registrar().CoRegisterClassObject(Test1.CLSID(), Test1.ProgID, Test1Factory())
