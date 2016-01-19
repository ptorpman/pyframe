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
from iunknown import IUnknown 
from uuid import UUID
from interfaces.iid    import IID

from abc import ABCMeta, abstractmethod


class ISchedulerServer(IUnknown):
    ''' Interface implemented by the Scheduler component '''
    @staticmethod
    def IID_ISchedulerServer():
        return IID('ISchedulerServer', UUID('{de04984d-d23c-448e-b1e8-b799067abd44}'))
    
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abstractmethod
    def AddScheduledComponent(self, comp): 
        ''' Add a component that wants scheduling. '''
        pass

    @abstractmethod
    def RemoveScheduledComponent(self, comp): 
        ''' Remove a component that was scheduled. '''
        pass


class ISchedulerClient(IUnknown):
    ''' Interface implemented by a component that wants scheduling '''
    @staticmethod
    def IID_ISchedulerClient():
        return IID('ISchedulerClient', UUID('{ca3bef4f-19cf-4c32-ae01-0b5f71ff1d38}'))
    
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abstractmethod
    def Execute(self, slice): 
        ''' Add a component that wants scheduling. '''
        pass
    

