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
            cls._commands['help']   = cls._instance.help
            cls._commands['create'] = cls._instance.create
            cls._commands['list']   = cls._instance.list_cmd

            return cls._instance

        return cls._instance

    def __init__(self):
        pass

    def handle_command(self, cmd_string):
        ''' Handle a command line argument '''
        argv = cmd_string.split(' ')

        if not self._commands.has_key(argv[0]):
            raise Exception('ERROR: Unknown command - %s' % argv[0])

        return self._commands[argv[0]](argv)

    def help(self, argv):
        ''' Command for displaying help '''
        if len(argv) == 1:
            print 'Available commands:'
            for cmd in self._commands:
                print cmd
            return

        if len(argv) == 2:
            if not self._commands.has_key(argv[1]):
                print 'Usage: help [<command>]'
                return

            self._commands[argv[1]](None, show_help = True)


    def create(self, argv, show_help = False):
        ''' Command for creating a component instance '''
        
        if show_help or len(argv) != 3:
            print 'Usage: create <CLSID>|<ProgID> <name>'
            return

        try:
            use_id = argv[1]
            if '.' in use_id:
                # User is using ProgID
                use_id = Registrar().CLSIDFromProgID(use_id)

            cls_obj = Registrar().CoGetClassObject(use_id, 
                                                   IClassFactory.IID_IClassFactory())
            inst = cls_obj.CreateInstance(argv[2])

        except Exception as exc:
            print 'ERROR: Could not find class object for - %s (%s)' % (argv[1], exc)
            return
            
    def list_cmd(self, argv, show_help = False):
        ''' Command for listing information '''

        if show_help or len(argv) != 2:
            print 'Usage: list [--clsid]'
            return
            
        Registrar().print_registered_clsid()



