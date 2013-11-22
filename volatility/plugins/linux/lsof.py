# Volatility
# Copyright (C) 2007-2013 Volatility Foundation
#
# This file is part of Volatility.
#
# Volatility is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 2 as
# published by the Free Software Foundation.  You may not use, modify or
# distribute this program under any other version of the GNU General
# Public License.
#
# Volatility is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Volatility.  If not, see <http://www.gnu.org/licenses/>.
#

"""
@author:       Andrew Case
@license:      GNU General Public License 2.0
@contact:      atcuno@gmail.com
@organization:
"""
from volatility.plugins.linux import common


class Lsof(common.LinProcessFilter):
    """Lists open files."""

    __name = "lsof"

    def lsof(self):
        for task in self.filter_processes():
            # The user space file descriptor is simply the offset into the fd
            # array.
            for i, file_ptr in enumerate(task.files.fds):
                file_struct = file_ptr.deref()
                if file_struct:
                    yield (task, file_struct, i)

    def render(self, renderer):

        renderer.table_header([("Pid", "pid", "8"),
                               ("FD", "fd", "8"),
                               ("Path", "path", "")])

        for (task, file_struct, fd) in self.lsof():
            renderer.table_row(task.pid, fd, task.get_path(file_struct))