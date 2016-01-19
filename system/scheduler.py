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

from uuid import UUID

from interfaces.iunknown   import IUnknown
from interfaces.ischeduler import ISchedulerServer, ISchedulerClient
from common.exceptions     import NoReferencesException
from system.trace          import Trace
from system.timers         import PeriodicTimer
from interfaces.iid        import IID
from common.component      import ComponentBase

class Scheduler(ComponentBase, ISchedulerServer):
    ''' The singleton scheduler of the system '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Scheduler, cls).__new__(cls, *args, **kwargs)
            cls._scheduled_instances = []
            cls._timer = None
            return cls._instance

        return cls._instance

    def __init__(self):
        interfaces = [ISchedulerServer.IID_ISchedulerServer()]
        super(Scheduler, self).__init__('Scheduler', interfaces)

    
    # ISchedulerServer methods
    def AddScheduledComponent(self, comp):
        ''' Add a component that wants scheduling. '''
        iface = comp.QueryInterface(ISchedulerClient.IID_ISchedulerClient())
        self._scheduled_instances.append(iface)

    def RemoveScheduledComponent(self, comp): 
        ''' Remove a component that was scheduled. '''
        self._scheduled_instances.remove(comp)
    
    def Start(self):
        ''' Starts the scheduling loop '''
        Trace().logger().debug("Scheduler started...")
        self._timer = PeriodicTimer(0.01, self.slice)
        self._timer.start()

    def Stop(self):
        ''' Stops the scheduling loop '''
        Trace().logger().debug("Scheduler stopped...")
        self._timer.stop()
        
    def slice(self):
        ''' Callback when timer fires '''
        for c in self._scheduled_instances:
            c.Execute(0.01)
    
    
