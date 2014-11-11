from abc import ABCMeta, abstractmethod
from uuid import UUID
from common.exceptions import NoReferencesException

class IUnknown(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def IID_IUnknown(): return UUID('{00000000-0000-0000-C000-000000000046}')
    @staticmethod
    def version(): return '1.0'

    @abstractmethod
    def QueryInterface(self, iid): pass

    @abstractmethod
    def AddRef(self, iid):  pass

    @abstractmethod
    def Release(self, iid):  pass

    
    
    
