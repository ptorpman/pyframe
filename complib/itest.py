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
import abc
from uuid import UUID

from interfaces.iunknown import IUnknown
from interfaces.iid      import IID

class ITest(IUnknown):
    __metaclass__ = abc.ABCMeta

    name = 'ITest'
    
    @classmethod
    def IID_ITest(cls):
        return IID('ITest', UUID('{10000000-0000-0000-C000-000000000046}'))
    
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abc.abstractmethod
    def test_me(self): pass
