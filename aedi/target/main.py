#
#    Helper module to build macOS version of various radio frequency tools
#    Copyright (C) 2020-2025 Alexey Lysiuk
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import shutil

from ..state import BuildState
from . import base


class MakeMainTarget(base.MakeTarget):
    def __init__(self, name=None):
        super().__init__(name)

        self.destination = self.DESTINATION_OUTPUT


class CMakeMainTarget(base.CMakeTarget):
    def __init__(self, name=None):
        super().__init__(name)

        self.destination = self.DESTINATION_OUTPUT
        self.outputs = (self.name + '.app',)

    def post_build(self, state: BuildState):
        if state.xcode:
            return

        if state.install_path.exists():
            shutil.rmtree(state.install_path)

        os.makedirs(state.install_path)

        for output in self.outputs:
            src = state.build_path / output
            dst_sep_pos = output.rfind(os.sep)
            dst = state.install_path / (output if dst_sep_pos == -1 else output[dst_sep_pos + 1:])

            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)


class CMakeSingleExeMainTarget(CMakeMainTarget):
    def __init__(self, name=None):
        super().__init__(name)
        self.outputs = (name,)
