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
from threading import Timer

class PeriodicTimer(object):
    ''' Periodic timer '''
    def __init__(self, interval, callback, **kwargs):
        ''' Constructor '''
        self._timer     = None
        self.interval   = interval
        self.callback   = callback
        self.kwargs     = kwargs

    def _run(self):
        self.callback(**self.kwargs)
        self._timer = Timer(self.interval, self._run)
        self._timer.start()

    def start(self):
        if self._timer:
            return
        
        self._timer = Timer(self.interval, self._run)
        self._timer.start()
        self.is_running = True

    def stop(self):
        if not self._timer:
            return
        self._timer.cancel()
        self._timer = None
