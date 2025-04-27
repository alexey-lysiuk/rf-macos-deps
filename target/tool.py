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

import aedi.target.base as base
from aedi.state import BuildState


class DfuUtilTarget(base.ConfigureMakeDependencyTarget):
    def __init__(self, name='dfu-util'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://dfu-util.sourceforge.net/releases/dfu-util-0.11.tar.gz',
            'b4b53ba21a82ef7e3d4c47df2952adf5fa494f499b6b0b57c58c5d04ae8ff19e')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('src/dfu_util.h')


class HackRFTarget(base.CMakeSharedDependencyTarget):
    _VERSION = '2024.02.1'

    def __init__(self, name='hackrf'):
        super().__init__(name)
        self.src_root = 'host'

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/greatscottgadgets/hackrf/releases/download/'
            f'v{HackRFTarget._VERSION}/hackrf-{HackRFTarget._VERSION}.tar.xz',
            'd9ced67e6b801cd02c18d0c4654ed18a4bcb36c24a64330c347dfccbd859ad16')

    def configure(self, state: BuildState):
        state.options['RELEASE'] = HackRFTarget._VERSION
        super().configure(state)
