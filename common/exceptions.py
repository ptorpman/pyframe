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

class NoSuchCommand(Exception):
    ''' Exception raised when a non-existing command is called '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'NoSuchCommand: %s' % self.output

class CliArgException(Exception):
    ''' Exception raised when a command is used improperly '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'CliArgException: %s' % self.output
    

class NoReferencesException(Exception):
    ''' Exception raised when all references to an instances are removed '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'NoReferencesException: %s' % self.output

class NoInterfaceException(Exception):
    ''' Exception raised when an interface is not supported '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'NoInterfaceException: %s' % self.output

class TooManyReleaseException(Exception):
    ''' Exception raised when an interfaces has been released one too many times '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'TooManyReleaseException: %s' % self.output

