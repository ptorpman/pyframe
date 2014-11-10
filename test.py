import interfaces
from interfaces.iunknown      import IUnknown
from interfaces.iclassfactory import IClassFactory

from registrar import Registrar

class TestFactory(object):
    def __init__(self):
        self.iclassfactory = IClassFactory(self)
        self.iclassfactory.CreateInstance = self._CreateInstance
        self.iclassfactory.LockServer     = self._LockServer

        self.iunknown = IUnknown(
            self, 
            { IClassFactory.IID_IClassFactory(): self.iclassfactory })
        
    def _CreateInstance(self, iid): 
        return Test(iid)

    def _LockServer(self, block): 
        pass

class ITest(object):
    @staticmethod
    def IID_ITest(): return '10000000-0000-0000-C000-000000000046'

    def __init__(self, parent):
        self._parent = parent

    def test_me(self):
        print "Test me!"



class Test(object):
    def __init__(self, name):
        self.name = name

        self.itest    = ITest(self)

        supported_interfaces = { ITest.IID_ITest(): self.itest }

        self.iunknown = IUnknown(self, supported_interfaces)


if __name__ == '__main__':

    Registrar().CoRegisterClassObject('123', TestFactory())

    try:
        Registrar().CoRegisterClassObject('123', TestFactory())
    except Exception as exc:
        print "Got expected exception"

    clsobj = Registrar().CoGetClassObject('123', IClassFactory.IID_IClassFactory())
    print clsobj

    inst1 = clsobj.CreateInstance('001')
    print inst1

    inst2 = clsobj.CreateInstance('002')
    print inst2
    
    print inst1.iunknown.QueryInterface(IUnknown.IID_IUnknown())
    inst1.iunknown.AddRef(IUnknown.IID_IUnknown())
    inst1.iunknown.Release(IUnknown.IID_IUnknown())
    print inst1.iunknown.QueryInterface(ITest.IID_ITest())
    inst1.iunknown.Release(IUnknown.IID_IUnknown())
    print inst1
