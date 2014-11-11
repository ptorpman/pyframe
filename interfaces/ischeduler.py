from iunknown import IUnknown 
from uuid import UUID

from abc import ABCMeta, abstractmethod


class ISchedulerServer(IUnknown):
    ''' Interface implemented by the Scheduler component '''
    @staticmethod
    def IID_IClassFactory(): return UUID('{de04984d-d23c-448e-b1e8-b799067abd44}')
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abstractmethod
    def AddScheduledComponent(self, comp): 
        ''' Add a component that wants scheduling. '''
        pass

    @abstractmethod
    def RemoveScheduledComponent(self, comp): 
        ''' Remove a component that was scheduled. '''
        pass


class ISchedulerClient(IUnknown):
    ''' Interface implemented by a component that wants scheduling '''
    @staticmethod
    def IID_IClassFactory(): return UUID('{ca3bef4f-19cf-4c32-ae01-0b5f71ff1d38}')
    @staticmethod
    def version(): return '1.0'

    def __init__(self, parent):
        self._parent = parent

    @abstractmethod
    def Execute(self, slice): 
        ''' Add a component that wants scheduling. '''
        pass
    

