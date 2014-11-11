from iunknown import IUnknown 
from uuid import UUID

from abc import ABCMeta, abstractmethod

class IClassFactory(IUnknown):
    __metaclass__ = ABCMeta

    @staticmethod
    def IID_IClassFactory(): return UUID('{00000001-0000-0000-C000-000000000046}')
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abstractmethod
    def CreateInstance(self, iid): pass

    @abstractmethod
    def LockServer(self, block): pass
