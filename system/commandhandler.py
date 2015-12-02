# -*- mode: Python; fill-column: 75; comment-column: 70; -*-
#
#  This file is part of Torpman's PyFrame 
#         https://github.com/ptorpman/pyframe
# 
#  This sofware is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
# 
#  This software is distributed in the hope that it will 
#  be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.or/licenses/>.
#
#  Author: Peter R. Torpman (peter at torpman dot se)
#
#------------------------------------------------------------------------------
import imp
import os
import json

from common.exceptions        import NoSuchCommand
from system.registrar         import Registrar
from interfaces.iclassfactory import IClassFactory
from interfaces.iconfig       import IConfig

class CommandHandler(object):
    ''' The singleton that handles the global commands of PyFrame '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CommandHandler, cls).__new__(cls, *args, **kwargs)
            cls._commands = {}
            cls._commands['help']    = cls._instance.help
            cls._commands['create']  = cls._instance.create_cmd
            cls._commands['delete']  = cls._instance.delete_cmd
            cls._commands['list']    = cls._instance.list_cmd
            cls._commands['load']    = cls._instance.load_cmd
            cls._commands['config']  = cls._instance.config_cmd
            cls._commands['connect'] = cls._instance.connect_cmd

            return cls._instance

        return cls._instance

    def __init__(self):
        pass

    def handle_command(self, cmd_string):
        ''' Handle a command line argument '''
        argv = cmd_string.split(' ')

        if not self._commands.has_key(argv[0]):
            raise NoSuchCommand('ERROR: Unknown command - %s' % argv[0])

        return self._commands[argv[0]](argv)

    def help(self, argv):
        ''' Command for displaying help '''
        if len(argv) == 1:
            print 'Available commands:'
            for cmd in sorted(self._commands):
                print cmd
            return

        if len(argv) == 2:
            if not self._commands.has_key(argv[1]):
                print 'Usage: help [<command>]'
                return

            self._commands[argv[1]](None, show_help = True)


    def create_cmd(self, argv, show_help = False):
        ''' Command for creating a component instance '''
        
        if show_help or len(argv) != 3:
            print 'Usage: create <CLSID>|<ProgID> <name>'
            return

        try:
            use_id = argv[1]
            if '.' in use_id:
                # User is using ProgID
                use_id = Registrar().CLSIDFromProgID(use_id)

            cls_obj = Registrar().CoGetClassObject(use_id, IClassFactory.IID_IClassFactory())
            inst = cls_obj.CreateInstance(use_id, argv[2])

            Registrar().AddInstance(argv[2], argv[1], inst)

        except Exception as exc:
            raise
            print 'ERROR: Could not find class object for - %s (%s)' % (argv[1], exc)
            return
            
    def delete_cmd(self, argv, show_help = False):
        ''' Command for deleting instances '''

        if show_help or len(argv) != 2:
            print 'Usage: delete <name>'
            return

        Registrar().RemoveInstance(argv[1])

        
    def list_cmd(self, argv, show_help = False):
        ''' Command for listing information '''
        
        if show_help:
            print 'Usage: list [--clsid]'
            return

        if len(argv) > 1:
            if argv[1] != '--clsid':
                print 'Usage: list [--clsid]'
                return

            Registrar().print_registered_clsid()
            return

        Registrar().print_instances()


    def config_cmd(self, argv, show_help = False):
        ''' Command for configuring a component '''

        if show_help:
            print 'Usage: config <name> <json-string>'
            return

        print argv
        

    def connect_cmd(self, argv, show_help = False):
        ''' Command for connecting a component to an other '''

        if show_help:
            print 'Usage: config <name1> <name2> <interface>'
            return
        
        

        
    def load_cmd(self, argv, show_help = False):
        ''' Command for loading configuration '''

        if show_help or len(argv) != 2:
            print 'Usage: load <file>'
            return
            
        try:
            config = {}
            with open(argv[1], 'r') as aFile:
                config = json.load(aFile)
                
                for cmd in config.keys():
                    if cmd == 'create':
                        for use_id in config[cmd].keys():
                            argv = {}

                            for i in range(len(config[cmd][use_id])):
                                inst = config[cmd][use_id][i]
                                argv[0] = 'create'
                                argv[1] = str(use_id)
                                argv[2] = str(inst)

                                self.create_cmd(argv)

                    elif cmd == 'config':
                        print config[cmd].keys()
                        for use_id in config[cmd].keys():
                            inst = Registrar().GetInstance(use_id)

                            if not inst:
                                raise Exception('Instance called "%s" does not exist' % use_id)

                            iface = inst.QueryInterface(IConfig.IID_IConfig())
                            print iface
                            iface.Configure(config[cmd][use_id])



        except Exception as exc:
            raise
            print "ERROR: Failed to load configuration. Exception: %s" % exc



