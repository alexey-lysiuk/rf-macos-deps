#
#    Module to build radio frequency libraries and tools for macOS
#    Copyright (C) 2025 Alexey Lysiuk
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

from aedi.state import BuildState
from aedi.target.base import CMakeMainTarget


class SdrPlusPlusTarget(CMakeMainTarget):
    def __init__(self, name='sdrpp'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.checkout_git('https://github.com/AlexandreRouma/SDRPlusPlus.git')

    def configure(self, state: BuildState):
        opts = state.options
        opts['OPT_BUILD_AIRSPY_SOURCE'] = 'NO'
        opts['OPT_BUILD_AIRSPYHF_SOURCE'] = 'NO'
        opts['OPT_BUILD_AUDIO_SOURCE'] = 'NO'
        opts['OPT_BUILD_AUDIO_SINK'] = 'NO'

        super().configure(state)
