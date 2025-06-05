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


class OrcTarget(base.MesonSharedTarget):
    def __init__(self, name='orc'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://gstreamer.freedesktop.org/src/orc/orc-0.4.41.tar.xz',
            'cb1bfd4f655289cd39bc04642d597be9de5427623f0861c1fc19c08d98467fa2')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('orc/orc.h')

    def configure(self, state: BuildState):
        opts = state.options
        opts['benchmarks'] = 'disabled'
        opts['examples'] = 'disabled'
        opts['orc-test'] = 'disabled'
        opts['tests'] = 'disabled'

        super().configure(state)


class Rtl433Target(base.CMakeDependencyTarget):
    def __init__(self, name='rtl433'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/merbanan/rtl_433/archive/refs/tags/25.02.tar.gz',
            '5a409ea10e6d3d7d4aa5ea91d2d6cc92ebb2d730eb229c7b37ade65458223432',
            patches=('rtl433-force-version', 'rtl433-no-abspath'))
