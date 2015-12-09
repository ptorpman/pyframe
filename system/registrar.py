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

from interfaces.iunknown import IUnknown
from common.exceptions   import NoReferencesException
from system.trace        import Trace

class Registrar(object):
    ''' The singleton registrar of the system '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registrar, cls).__new__(cls, *args, **kwargs)
            cls._instance.class_objects = {}
            cls._instance.prog_ids = {}
            cls._comp_instances = {}

            return cls._instance

        return cls._instance

    def __init__(self):
        pass

    def CoRegisterClassObject(self, clsid, progid, instance):
        ''' Register a class object/factory '''

        if self.class_objects.has_key(clsid) or self.prog_ids.has_key(progid):
            raise Exception('Class object already registered: CLSID=%s ProgID=%s' % \
                            (clsid, progid))

        
        self.class_objects[clsid] = instance
        self.prog_ids[clsid]      = progid
        Trace().debug("Added class object for CLSID: %s (%s)" % (clsid, progid))

    def CoGetClassObject(self, clsid, iid):
        ''' Return class object for a CLSID '''

        use_clsid = clsid
        if isinstance(clsid, str):
            use_clsid = UUID('{%s}' % clsid)

        if not self.class_objects.has_key(use_clsid):
            raise Exception('No class object registered for: %s' % use_clsid)

        return self.class_objects[use_clsid].QueryInterface(iid)

    def print_registered_clsid(self):
        ''' Returns a list of registered CLSIDs '''
    
        val = []
        for obj in self.class_objects:
            val.append((str(obj), self.class_objects[obj]))

        print '%-45s %-32s %s' % ('Class ID', 'ProgID', 'Class Object')
        print '-' * 100

        for clsid in val:
            print '%-45s %-32s %s' % (clsid[0], self.prog_ids[UUID('{%s}' % clsid[0])], clsid[1])

    def print_instances(self):
        ''' Print all created instances '''

        if not self._comp_instances:
            print "* No instances created."
            return

        print '%-30s %-32s %s' % ('Instance', 'ProgID', 'CLSID')
        print '-' * 100

        for comp in sorted(self._comp_instances.keys()):
            print '%-30s %-32s %s' % (comp, self.ProgIDFromCLSID(self._comp_instances[comp][0]),
                                      self._comp_instances[comp][0])

    def CLSIDFromProgID(self, progid):
        ''' Returns CLSID for a ProgID '''
        for c in self.prog_ids:
            if self.prog_ids[c] == progid:
                return c

        return None

    def ProgIDFromCLSID(self, clsid):
        ''' Returns a ProgID for a CLSID '''
        if self.prog_ids.has_key(clsid):
            return self.prog_ids[clsid]
            
        return None

    def AddInstance(self, name, used_id, instance):
        ''' Add component instance '''

        if self._comp_instances.has_key(name):
            raise Exception('Component called "%s" already exists' % name)
        
        self._comp_instances[name] = [ used_id, instance ]
        instance.AddRef(IUnknown.IID_IUnknown())

    def GetInstance(self, name):
        ''' Return component instance with name '''
        if not self._comp_instances.has_key(name):
            return None

        return self._comp_instances[name][1]
        
    def RemoveInstance(self, name):
        ''' Delete component instance '''
        if not self._comp_instances.has_key(name):
            raise Exception('Instance %s does not exist' % name)

        try:
            self._comp_instances[name][1].Release(IUnknown.IID_IUnknown())
        except NoReferencesException as exc:
            # No more references left
            del self._comp_instances[name]
            
