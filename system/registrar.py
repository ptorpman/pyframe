
from uuid import UUID


class Registrar(object):
    ''' The singleton registrar of the system '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registrar, cls).__new__(cls, *args, **kwargs)
            cls._instance.class_objects = {}
            cls._instance.prog_ids = {}
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
        print "* Added class object for CLSID: %s (%s)" % (clsid, progid)

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
