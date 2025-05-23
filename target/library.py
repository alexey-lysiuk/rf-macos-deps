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

import os
import shutil

import aedi.target.base as base
from aedi.state import BuildState


class Ad9361Target(base.CMakeSharedDependencyTarget):
    def __init__(self, name='ad9361'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            # libad9361-iio v0.3 with addition of CMake option to disable macOS framework
            # https://github.com/analogdevicesinc/libad9361-iio/commit/ef3d58506132072834637f887bc47eb4d0c52a73
            # https://github.com/analogdevicesinc/libad9361-iio/commit/05fbfed2b2104645a6ebe262631bb35a09c73a37
            'https://github.com/analogdevicesinc/libad9361-iio/archive/05fbfed2b2104645a6ebe262631bb35a09c73a37.tar.gz',
            '10f7124ee77e5d1987733dce86c7d572917c16c69023d78a932298f8e8b22552')

    def configure(self, state: BuildState):
        state.options['OSX_FRAMEWORK'] = 'NO'
        super().configure(state)


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


class GlfwTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='glfw'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/glfw/glfw/archive/refs/tags/3.4.tar.gz',
            'c038d34200234d071fae9345bc455e4a8f2f544ab60150765d7704e08f3dac01',
            patches='glfw-fix-vsync')

    def configure(self, state: BuildState):
        opts = state.options
        opts['GLFW_BUILD_EXAMPLES'] = 'NO'
        opts['GLFW_BUILD_TESTS'] = 'NO'

        super().configure(state)


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


class IioTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='iio'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/analogdevicesinc/libiio/archive/refs/tags/v0.26.tar.gz',
            'fb445fb860ef1248759f45d4273a4eff360534480ec87af64c6b8db3b99be7e5')

    def configure(self, state: BuildState):
        state.options['OSX_FRAMEWORK'] = 'NO'
        super().configure(state)


class MakoTarget(base.BuildTarget):
    def __init__(self, name='mako'):
        super().__init__(name)
        self.multi_platform = False

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/sqlalchemy/mako/archive/refs/tags/rel_1_3_10.tar.gz',
            'e8f1334904611d5cb357b6396790fd4375ac21ad901f4314d222d5d5758979b9')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('mako/ast.py')

    def post_build(self, state: BuildState):
        shutil.copytree(state.source / self.name, state.install_path / 'lib/python' / self.name)


class MarkupSafeTarget(base.BuildTarget):
    def __init__(self, name='markupsafe'):
        super().__init__(name)
        self.multi_platform = False

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/pallets/markupsafe/releases/download/3.0.2/markupsafe-3.0.2.tar.gz',
            'ee55d3edf80167e48ea11a923c7386f4669df67d7994554387f84e7d8b0a2bf0')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('markupsafe/_native.py')

    def post_build(self, state: BuildState):
        dest_path = state.install_path / 'lib/python' / self.name
        os.makedirs(dest_path)

        for filename in ('__init__.py', '_native.py'):
            shutil.copy(state.source / 'src' / self.name / filename, dest_path)


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


class VolkTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='volk'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/gnuradio/volk/releases/download/v3.2.0/volk-3.2.0.tar.gz',
            '9c6c11ec8e08aa37ce8ef7c5bcbdee60bac2428faeffb07d072e572ed05eb8cd',
            patches='volk-no-abspaths')

    def configure(self, state: BuildState):
        opts = state.options
        opts['ENABLE_MODTOOL'] = 'NO'
        opts['ENABLE_TESTING'] = 'NO'

        super().configure(state)

    def post_build(self, state: BuildState):
        super().post_build(state)

        # Patch CMake module to replace absolute path
        soname_prefix = '  IMPORTED_SONAME_RELEASE '
        soname_path = soname_prefix + '"${CMAKE_CURRENT_LIST_DIR}/../../libvolk.3.2.dylib"\n'

        def update_path(line: str):
            return soname_path if line.startswith(soname_prefix) else line

        cmake_module = state.install_path / 'lib/cmake/volk/VolkTargets-release.cmake'
        self.update_text_file(cmake_module, update_path)


class ZstdTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='zstd'):
        super().__init__(name)
        self.src_root = 'build/cmake'

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/facebook/zstd/releases/download/v1.5.7/zstd-1.5.7.tar.gz',
            'eb33e51f49a15e023950cd7825ca74a4a2b43db8354825ac24fc1b7ee09e6fa3')

    def configure(self, state: BuildState):
        opts = state.options
        opts['ZSTD_BUILD_PROGRAMS'] = 'NO'
        opts['ZSTD_BUILD_STATIC'] = 'NO'

        super().configure(state)
