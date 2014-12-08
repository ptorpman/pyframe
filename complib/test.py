#--------------------------------------------------------------------
# COMPONENT CLASSES 
#--------------------------------------------------------------------
import abc
from uuid import UUID

from common.component import ComponentBase
from common.exceptions import NoReferencesException
from interfaces.iunknown      import IUnknown
from interfaces.iclassfactory import IClassFactory


class TestFactory(ComponentBase, IClassFactory):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TestFactory, cls).__new__(cls, *args, **kwargs)
            cls._instance.name = "TestFactory"
            return cls._instance

        return cls._instance

    def __init__(self):
        super(TestFactory, self).__init__('TestFactory', 
                                          [IClassFactory.IID_IClassFactory()])

    # IClassFactory methods
    def CreateInstance(self, iid, name): 
        # FIXME: Check IID!
        return Test(name)

    def LockServer(self, block): 
        pass

class ITest(IUnknown):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def IID_ITest(cls): return UUID('{10000000-0000-0000-C000-000000000046}')
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abc.abstractmethod
    def test_me(self): pass



class Test(ComponentBase, ITest):

    ProgID = 'test.Test.1'

    @classmethod
    def CLSID_Test(cls): return UUID('{a70f9a02-699e-11e4-96dd-0800277e7e72}')

    def __init__(self, name):
        super(Test, self).__init__(name, [ITest.IID_ITest()])
    def test_me(self):
        print '%s: Test me!' % self



#--------------------------------------------------------------------
# COMPONENT REGISTRATION METHODS
#--------------------------------------------------------------------

def load_this():
    ''' To be called by CompLoader '''

    print 'DEBUG: Loading file... %s' % __file__
    from system.registrar import Registrar
    Registrar().CoRegisterClassObject(Test.CLSID_Test(), Test.ProgID, TestFactory())
