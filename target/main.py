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
        disabled_options = (
            'AIRSPY_SOURCE',
            'AIRSPYHF_SOURCE',
            'AUDIO_SOURCE',
            'AUDIO_SINK',
            'DISCORD_PRESENCE',
        )

        for option in disabled_options:
            opts['OPT_BUILD_' + option] = 'NO'

        super().configure(state)
