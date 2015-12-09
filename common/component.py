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
from interfaces.iunknown  import IUnknown
from common.exceptions    import NoInterfaceException
from common.exceptions    import NoReferencesException
from common.exceptions    import TooManyReleaseException
from system.trace         import Trace

class ComponentBase(IUnknown):
    ''' Base class for components in PyFrame ''' 
    def __init__(self, name, supported_iids):
        self.name           = name
        self._interfaces     = {}
        
        self._interfaces[IUnknown.IID_IUnknown()] = 0

        for i in supported_iids:
            self._interfaces[i] = 0

    def __str__(self):
        ''' String representation of component '''
        return self.name


    #-------------------------------------------------------------------------
    # IUnknown implementation
    #-------------------------------------------------------------------------
    def QueryInterface(self, iid): 
        ''' Return pointer to correct interface '''
        
        if not self._interfaces.has_key(iid): 
            raise NoInterfaceException('Interface %s not supported' % iid)

        Trace().debug("QueryInterface: AddRef().%s %s: %d" % (self.name, iid, self._interfaces[iid]))
        self.AddRef(iid)
        return self

    def AddRef(self, iid): 
        ''' Add reference to interface '''
        if not self._interfaces.has_key(iid): 
            raise NoInterfaceException('Interface %s not supported' % iid)

        self._interfaces[iid] = self._interfaces[iid] + 1
        Trace().debug("AddRef().%s %s: %d" % (self.name, iid, self._interfaces[iid]))

    def Release(self, iid): 
        ''' Remove reference from interface '''
        if not self._interfaces.has_key(iid): 
            raise NoInterfaceException('Interface %s not supported' % iid)

        self._interfaces[iid] = self._interfaces[iid] - 1

        if self._interfaces[iid] < 0:
            raise TooManyReleaseException('%s released too many times' % iid)

        if  set(self._interfaces.values()) == set([0]):
            Trace().debug("Release(): No refs left. Deleting...")
            raise NoReferencesException('%s: No references left.' % self.name)
        else:
            Trace().debug("Release() %s: %s" % (iid, self._interfaces[iid]))

