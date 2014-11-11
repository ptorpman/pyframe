import imp
import os

from system.registrar import Registrar
from interfaces.iclassfactory import IClassFactory

class CommandHandler(object):
    ''' The singleton that handles the global commands of PyFrame '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CommandHandler, cls).__new__(cls, *args, **kwargs)
            cls._commands = {}
            cls._commands['create'] = cls._instance.create
            cls._commands['list']   = cls._instance.list_cmd

            return cls._instance

        return cls._instance

    def __init__(self):
        print "CommandHandler initialized"
        pass

    def handle_command(self, cmd_string):
        ''' Handle a command line argument '''
        argv = cmd_string.split(' ')

        if not self._commands.has_key(argv[0]):
            print 'ERROR: Unknown command - %s' % argv[0]
            return

        return self._commands[argv[0]](argv)

    def create(self, argv):
        ''' Command for creating a component instance '''

        if len(argv) != 3:
            print 'Usage: create <CLSID> <name>'
            return

        try:
            cls_obj = Registrar().CoGetClassObject(argv[1], 
                                                   IClassFactory.IID_IClassFactory())
            inst = cls_obj.CreateInstance(argv[2])

        except Exception as exc:
            print 'ERROR: Could not find class object for - %s (%s)' % (argv[1], exc)
            return
            
    def list_cmd(self, argv):
        ''' Command for listing information '''

        if len(argv) != 2:
            print 'Usage: list [--clsid]'
            return
            
        clsids = Registrar().get_registered_clsid()
        print '%-45s %s' % ('Class ID', 'Class Object')
        print '-' * 80

        for clsid in clsids:
            print '%-45s %s' % (clsid[0], clsid[1])



