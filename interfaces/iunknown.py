class IUnknown(object):

    @staticmethod
    def IID_IUnknown(): return '00000000-0000-0000-C000-000000000046'
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent, interfaces):
        ''' Initialize with a dictionary with instances of interfaces, indexed on IIDs'''
        self._parent         = parent
        self._interfaces     = {}
        self._interface_refs = {}

        self._interfaces[self.IID_IUnknown()]     = self
        self._interface_refs[self.IID_IUnknown()] = 0

        for i in interfaces:
            self._interfaces[i]     = interfaces[i]
            self._interface_refs[i] = 0

    def QueryInterface(self, iid): 
        ''' Return pointer to correct interface '''
        
        if not self._interfaces.has_key(iid): 
            raise NotImplemented
        else:
            return self._interfaces[iid]

    def AddRef(self, iid): 
        ''' Add reference to interface '''
        if not self._interfaces.has_key(iid): 
            raise NotImplemented

        self._interface_refs[iid] = self._interface_refs[iid] + 1
        print "AddRef(). %s: %d" % (iid, self._interface_refs[iid])

    def Release(self, iid): 
        ''' Remove reference from interface '''
        if not self._interfaces.has_key(iid): 
            raise NotImplemented

        self._interface_refs[iid] = self._interface_refs[iid] - 1

        if  set(self._interface_refs.values()) == set([0]):
            print "Release(): No refs left. Deleting..."
            del self._parent
        else:
            print "Release() %s: %s" % (iid, vals)

    
    
    
