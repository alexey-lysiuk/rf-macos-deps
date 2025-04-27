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


class FftwTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='fftw'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://fftw.org/fftw-3.3.10.tar.gz',
            '56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467')

    def configure(self, state: BuildState):
        opts = state.options
        opts['BUILD_TESTS'] = 'NO'
        opts['DISABLE_FORTRAN'] = 'YES'
        opts['ENABLE_FLOAT'] = 'YES'
        opts['ENABLE_THREADS'] = 'YES'

        if state.architecture() == 'x86_64':
            opts['ENABLE_SSE2'] = 'YES'
            opts['ENABLE_AVX'] = 'YES'
            opts['ENABLE_AVX2'] = 'YES'

        super().configure(state)

        # Patch config header to replace absolute path
        def clean_build_config(line: str):
            cfg_prefix = '#define FFTW_CC "'
            return f'{cfg_prefix}clang"\n' if line.startswith(cfg_prefix) else line

        self.update_text_file(state.build_path / 'config.h', clean_build_config)

    def post_build(self, state: BuildState):
        super().post_build(state)

        # Patch CMake module to replace absolute paths
        replacements = {
            'set (FFTW3f_INCLUDE_DIRS ': '"${CMAKE_CURRENT_LIST_DIR}/../../../include")\n',
            'set (FFTW3f_LIBRARY_DIRS ': '"${CMAKE_CURRENT_LIST_DIR}/../../")\n'
        }

        def update_dirs(line: str):
            for prefix in replacements:
                if line.startswith(prefix):
                    return prefix + replacements[prefix]

            return line

        cmake_module = state.install_path / 'lib/cmake/fftw3f/FFTW3fConfig.cmake'
        self.update_text_file(cmake_module, update_dirs)


class FobosTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='fobos'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/rigexpert/libfobos/archive/refs/tags/v.2.3.2.tar.gz',
            '4ad2f1268fd4f61796673fff0c6abe3e718dc80f8e3c14e649f6b15c9a8bd0f1',
            patches=('fobos-fix-cmake', 'fobos-fix-determinism', 'fobos-fix-open'))

    def post_build(self, state: BuildState):
        super().post_build(state)

        for binary in ('fobos_devinfo', 'fobos_fwloader', 'fobos_recorder'):
            self.copy_to_bin(state, binary)


class RtlSdrTarget(base.CMakeDependencyTarget):
    def __init__(self, name='rtlsdr'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/steve-m/librtlsdr/archive/refs/tags/v2.0.2.tar.gz',
            'f407de0b6dce19e81694814e363e8890b6ab2c287c8d64c27a03023e5702fb42')
        
    def post_build(self, state: BuildState):
        super().post_build(state)

        # Patch CMake module to replace absolute paths
        replacements = {
            '  INTERFACE_INCLUDE_DIRECTORIES ':
                '"${_IMPORT_PREFIX}/include;${CMAKE_CURRENT_LIST_DIR}/../../../include/libusb-1.0"\n',
            '  INTERFACE_LINK_LIBRARIES ':
                '"${CMAKE_CURRENT_LIST_DIR}/../../libusb-1.0.dylib"\n',
        }

        def update_dirs(line: str):
            for prefix in replacements:
                if line.startswith(prefix):
                    return prefix + replacements[prefix]

            return line

        cmake_module = state.install_path / 'lib/cmake/rtlsdr/rtlsdrTargets.cmake'
        self.update_text_file(cmake_module, update_dirs)


class UsbTarget(base.ConfigureMakeSharedDependencyTarget):
    def __init__(self, name='usb'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/libusb/libusb/releases/download/v1.0.28/libusb-1.0.28.tar.bz2',
            '966bb0d231f94a474eaae2e67da5ec844d3527a1f386456394ff432580634b29')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('libusb/libusb.h')
