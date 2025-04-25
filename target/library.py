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


class UsbTarget(base.ConfigureMakeSharedDependencyTarget):
    def __init__(self, name='usb'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/libusb/libusb/releases/download/v1.0.28/libusb-1.0.28.tar.bz2',
            '966bb0d231f94a474eaae2e67da5ec844d3527a1f386456394ff432580634b29')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('libusb/libusb.h')
