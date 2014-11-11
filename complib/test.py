

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
    def __init__(self):
        super(TestFactory, self).__init__('TestFactory', 
                                          [IClassFactory.IID_IClassFactory()])

    # IClassFactory methods
    def CreateInstance(self, iid): 
        return Test(iid)

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

    @classmethod
    def CLSID_Test(cls): return UUID('{a70f9a02-699e-11e4-96dd-0800277e7e72}')

    def __init__(self, name):
        super(Test, self).__init__(name, 
                                   [ITest.IID_ITest()])
    def test_me(self):
        print '%s: Test me!' % self



#--------------------------------------------------------------------
# COMPONENT REGISTRATION METHODS
#--------------------------------------------------------------------

def load_this():
    ''' To be called by CompLoader '''

    print 'DEBUG: Loading file... %s' % __file__
    from system.registrar import Registrar
    Registrar().CoRegisterClassObject(Test.CLSID_Test(), TestFactory())
