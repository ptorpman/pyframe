from interfaces.iunknown  import IUnknown
from common.exceptions    import NoInterfaceException
from common.exceptions    import NoReferencesException
from common.exceptions    import TooManyReleaseException

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

        self.AddRef(iid)
        return self

    def AddRef(self, iid): 
        ''' Add reference to interface '''
        if not self._interfaces.has_key(iid): 
            raise NoInterfaceException('Interface %s not supported' % iid)

        self._interfaces[iid] = self._interfaces[iid] + 1
        print "AddRef().%s %s: %d" % (self.name, iid, self._interfaces[iid])

    def Release(self, iid): 
        ''' Remove reference from interface '''
        if not self._interfaces.has_key(iid): 
            raise NoInterfaceException('Interface %s not supported' % iid)

        self._interfaces[iid] = self._interfaces[iid] - 1

        if self._interfaces[iid] < 0:
            raise TooManyReleaseException('%s released too many times' % iid)

        if  set(self._interfaces.values()) == set([0]):
            print "Release(): No refs left. Deleting..."
            raise NoReferencesException('%s: No references left.' % self.name)
        else:
            print "Release() %s: %s" % (iid, self._interfaces[iid])

