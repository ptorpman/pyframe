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

import logging

class Trace(object):
    ''' The singleton handling tracing and logging '''
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Trace, cls).__new__(cls, *args, **kwargs)
            cls._log = logging.getLogger(__name__)
            cls._log_level = logging.INFO
            cls._logfile = None

            return cls._instance

        return cls._instance

    def __init__(self):
        pass

    def set_logging(self, use_debug = False, logfile = None):
        if use_debug:
            self._log_level = logging.DEBUG
            formatter = '%(levelname)s %(asctime)s - %(filename)s:%(lineno)s %(funcName)10s - %(message)s'
        else:
            self._log_level = logging.INFO
            formatter = '* %(message)s'

        self._logfile = logfile

        logging.basicConfig(level= self._log_level, format = formatter)

        self._log.debug('Setting up logger...')

        if self._logfile:
            fh = logging.FileHandler(self._logfile)
            fh.setLevel(self._log_level)
            fh.setFormatter(logging.Formatter(formatter))
            self._log.addHandler(fh)
        
    def logger(self):
        ''' Return the logger '''
        return self._log


    def debug(self, *args):
        ''' Print a debug statement '''
        self._log.debug(*args)
        
    def info(self, *args):
        ''' Print an info statement '''
        self._log.info(*args)

    
