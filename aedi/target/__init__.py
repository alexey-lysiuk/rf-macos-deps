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

from .library import *
from .main import *
from .special import *
from .tool import *


def targets():
    return (
        # Libraries
        FftwTarget(),
        FobosTarget(),
        GlfwTarget(),
        UsbTarget(),

        # Tools needed to build main targets and libraries
        CMakeTarget(),
        PkgConfigTarget(),

        # Special
        BuildPrefix(),
        CleanAllTarget(),
        CleanDepsTarget(),
        TestDepsTarget(),
    )
