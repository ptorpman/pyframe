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

import os
import rlcompleter
import readline
import subprocess
import traceback
import sys

from system.trace          import Trace
from system.comploader     import CompLoader
from system.commandhandler import CommandHandler
from common.exceptions     import NoSuchCommand

readline.parse_and_bind('tab: complete')

comp_libraries = [os.path.abspath(os.path.join(os.getcwd(), 'complib'))]

Trace().set_logging(use_debug = True, logfile = None)
Trace().info('Starting PyFrame...')

CompLoader().load_components(comp_libraries)
CommandHandler()

while True:
    # Wait for user input
    line = raw_input('pyframe # ')

    if line == 'exit' or line == 'quit' or  line == 'q':
        break
        
    try:
        CommandHandler().handle_command(line)
    except NoSuchCommand as exc:
        Trace().info('Executing shell command: %s' % line)
        os.system(line)
    except Exception as exc3:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print 'ERROR: %s' % exc3
        x = traceback.print_tb(exc_traceback)
