from iunknown import IUnknown 

class IClassFactory(IUnknown):
    @staticmethod
    def IID_IClassFactory(): return '00000001-0000-0000-C000-000000000046'
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    def CreateInstance(self, iid): 
        raise Exception('NotImplemented')

    def LockServer(self, block): 
        raise Exception('NotImplemented')
