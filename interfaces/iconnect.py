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

from abc import ABCMeta, abstractmethod
from interfaces.iid import IID


class IConnect(IUnknown):
    ''' Interface implemented by the all components that are connectable to others '''
    @staticmethod
    def IID_IConnect():
        return IID('IConnect', UUID('{8cf231c8-9f0f-11e5-a012-0800274bfca2}'))
    
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abstractmethod
    def Connect(self, instance, interface, arguments): 
        ''' Configure component. '''
        pass
