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
from interfaces.iid       import IID
from common.exceptions    import NoInterfaceException
from common.exceptions    import NoReferencesException
from common.exceptions    import TooManyReleaseException
from system.trace         import Trace
from system.registrar     import Registrar

class ComponentBase(IUnknown):
    ''' Base class for components in PyFrame ''' 
    def __init__(self, name, supported_iids):
        self.name             = name
        self._interface_names = {}
        self._interface_refs  = {}

        for iid in supported_iids:
            Trace().debug("%s supports interface: %s" % (name, iid.name))
            self._interface_names[iid.name] = iid.iid
            self._interface_refs[iid.name]  = 0
            Registrar().RegisterInterface(iid.name, iid.iid, self.name)

        # Safeguard to make sure IUnknown is always added
        if not self._interface_names.has_key('IUnknown'):
            iid = IUnknown.IID_IUnknown()
            self._interface_names[iid.name] = iid.iid
            self._interface_refs[iid.name]  = 0
            

            
        if hasattr(self, 'ProgID'):
            print self.ProgID

        op = getattr(self, 'CLSID', None)

        if callable(op):
            print 'CLSID: %s' % str(self.CLSID())
        

    def __str__(self):
        ''' String representation of component '''
        return self.name


    #-------------------------------------------------------------------------
    # IUnknown implementation
    #-------------------------------------------------------------------------
    def QueryInterface(self, iid): 
        ''' Return pointer to correct interface '''

        if isinstance(iid, IID):
            iface_name = iid.name
        else:
            iface_name = iid
        
        if not self._interface_names.has_key(iface_name): 
            raise NoInterfaceException('Interface %s not supported' % iface_name)

        Trace().debug("QueryInterface: AddRef().%s %s %d" % (self.name, iface_name, self._interface_refs[iface_name]))
        self.AddRef(iface_name)
        return self

    def AddRef(self, iid): 
        ''' Add reference to interface '''
        if isinstance(iid, IID):
            iface_name = iid.name
        else:
            iface_name = iid

        if not self._interface_names.has_key(iface_name): 
            raise NoInterfaceException('Interface %s not supported' % iface_name)

        self._interface_refs[iface_name] += 1
        Trace().debug("AddRef().%s %s: %d" % (self.name, iface_name, self._interface_refs[iface_name]))

    def Release(self, iid): 
        ''' Remove reference from interface '''

        if isinstance(iid, IID):
            iface_name = iid.name
        elif isinstance(iid, str):
            iface_name = iid
        else:
            raise Exception('Incorrect parameter')
        
        if not self._interface_names.has_key(iface_name): 
            raise NoInterfaceException('Interface %s not supported' % iface_name)

        self._interface_refs[iface_name] -= 1

        if self._interface_refs[iface_name] < 0:
            raise TooManyReleaseException('%s released too many times' % iface_name)

        if  set(self._interface_refs.values()) == set([0]):
            Trace().debug("Release(): No refs left. Deleting...")
            raise NoReferencesException('%s: No references left.' % self.name)
        else:
            Trace().debug("Release() %s: %s" % (iface_name, self._interface_refs[iface_name]))

