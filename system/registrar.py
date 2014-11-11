
from uuid import UUID


class Registrar(object):
    ''' The singleton registrar of the system '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registrar, cls).__new__(cls, *args, **kwargs)
            cls._instance.class_objects = {}
            return cls._instance

        return cls._instance

    def __init__(self):
        pass

    def CoRegisterClassObject(self, clsid, instance):
        ''' Register a class object/factory '''

        if self.class_objects.has_key(clsid):
            raise Exception('Class object already registered: %s' % clsid)

        
        self.class_objects[clsid] = instance
        print "* Added class object for CLSID: %s (%s)" % (clsid, type(clsid))

    def CoGetClassObject(self, clsid, iid):
        ''' Return class object for a CLSID '''

        use_clsid = clsid
        if isinstance(clsid, str):
            use_clsid = UUID('{%s}' % clsid)

        if not self.class_objects.has_key(use_clsid):
            raise Exception('No class object registered for: %s' % use_clsid)

        return self.class_objects[use_clsid].QueryInterface(iid)

    def get_registered_clsid(self):
        ''' Returns a list of registered CLSIDs '''
    
        val = []
        for obj in self.class_objects:
            val.append((str(obj), self.class_objects[obj]))

            return val
