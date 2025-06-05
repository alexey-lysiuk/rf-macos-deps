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
import subprocess
from pathlib import Path

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


class AirspyTarget(base.CMakeDependencyTarget):
    def __init__(self, name='airspy'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/airspy/airspyone_host/archive/refs/tags/v1.0.10.tar.gz',
            'fcca23911c9a9da71cebeffeba708c59d1d6401eec6eb2dd73cae35b8ea3c613')


class AirspyHFTarget(base.CMakeDependencyTarget):
    def __init__(self, name='airspyhf'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/airspy/airspyhf/archive/refs/tags/1.6.8.tar.gz',
            'cd1e5ae89e09b813b096ae4a328e352c9432a582e03fd7da86760ba60efa77ab')


class BladeRFTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='bladerf'):
        super().__init__(name)
        self.src_root = 'host'

    def prepare_source(self, state: BuildState):
        # Downloaded source code fails to compile because of missing Git submodules
        # state.download_source(
        #     'https://github.com/Nuand/bladeRF/archive/refs/tags/2023.02.tar.gz',
        #     '3bbac54ad7d6e35be31eb12393be5e7102a070fb1ddc176992d64a6a623670c7')

        if not state.source.exists():
            clone_args = ('git', 'clone', 'https://github.com/Nuand/bladeRF.git', state.source)
            subprocess.run(clone_args, check=True, env=state.environment)

        checkout_args = (
            ('checkout', '2023.02'),
            ('submodule', 'update', '--init', '--recursive')
        )

        for args in checkout_args:
            subprocess.run(('git', *args), check=True, cwd=state.source, env=state.environment)

        # Verify commit hash of checked out release tag
        head_args = ('git', 'rev-parse', 'HEAD')
        head_run = subprocess.run(head_args, check=True, cwd=state.source,
                                  env=state.environment, stdout=subprocess.PIPE)
        head_output = head_run.stdout.decode('ascii').strip()

        if head_output != '41ef63460956e833c9b321252245257ab3946055':
            raise RuntimeError('BladeRF commit does not match with the release tag')

    def configure(self, state: BuildState):
        opts = state.options

        # Disable libusb check as it fails to run due to lack of @rpath in test executable
        # Set the corresponding preprocessor macro explicitly
        opts['CMAKE_C_FLAGS'] += '-DHAVE_LIBUSB_GET_VERSION'
        opts['LIBUSB_SKIP_VERSION_CHECK'] = 'YES'

        # Set search prefix to avoid absolute paths to intermediate directories
        opts['LIBBLADERF_SEARCH_PREFIX_OVERRIDE'] = '/usr/local'

        # Do not fail build as compilation generates some warnings
        opts['TREAT_WARNINGS_AS_ERRORS'] = 'NO'

        # Mark as tagged/release build
        opts['VERSION_INFO_EXTRA'] = ''

        super().configure(state)


class Codec2Target(base.CMakeStaticDependencyTarget):
    def __init__(self, name='codec2'):
        super().__init__(name)
        self.multi_platform = False

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/drowe67/codec2/archive/refs/tags/1.2.0.tar.gz',
            'cbccae52b2c2ecc5d2757e407da567eb681241ff8dadce39d779a7219dbcf449')

    def configure(self, state: BuildState):
        state.options['BUILD_OSX_UNIVERSAL'] = 'YES'
        super().configure(state)


class CorrectTarget(base.CMakeDependencyTarget):
    def __init__(self, name='correct'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/quiet/libcorrect/archive/f5a28c74fba7a99736fe49d3a5243eca29517ae9.tar.gz',
            '5a4305aabe6c7d5b58f6677c41c54ad5e8d9003f7a5998f7344d93534e4c5760')

    def post_build(self, state: BuildState):
        super().post_build(state)

        os.unlink(state.install_path / 'lib/libcorrect.dylib')

        self.write_pc_file(state, filename='libcorrect.pc',
            description='C library for Convolutional codes and Reed-Solomon', version='0.0.0', libs='-lcorrect')


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
        # Unlike the corresponding tag, the following commit is the proper version 2.3.2
        state.download_source(
            'https://github.com/rigexpert/libfobos/archive/f202101d5cfd40c1fe177513e256d49950c7dd9a.tar.gz',
            'f5d81fcc12460cbe86fbc0e7a3691b5eb6455141f4d4b588659c6ab69b3cfb6c',
            patches=('fobos-fix-cmake', 'fobos-fix-open'))
        # Use commit datetime to have a deterministic build, see fobos_rx_get_api_info() function
        state.set_build_datetime(2025, 1, 20, 10, 6, 1)

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


class LimeSuiteTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='limesuite'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/myriadrf/LimeSuite/archive/refs/tags/v23.11.0.tar.gz',
            'fd8a448b92bc5ee4012f0ba58785f3c7e0a4d342b24e26275318802dfe00eb33')
        state.set_build_datetime(2024, 1, 23)

    def configure(self, state: BuildState):
        opts = state.options
        opts['ENABLE_EXAMPLES'] = 'NO'
        opts['LIME_SUITE_EXTVER'] = 'gc2d9e877'  # 'g' + 8 characters of release tag commit hash
        opts['LIME_SUITE_ROOT'] = '/usr/local'

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


class PerseusTarget(base.ConfigureMakeSharedDependencyTarget):
    def __init__(self, name='perseus'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/Microtelecom/libperseus-sdr/releases/download/v0.8.2/libperseus_sdr-0.8.2.tar.gz',
            '07e4b106374cf0d946f1df17a94eccbef7533d6320e528d9c7b60ac8d39e0d38',
            patches=('perseus-fix-build', 'perseus-version-test'))

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('perseus-sdr.h')

    def post_build(self, state: BuildState):
        super().post_build(state)

        test_exe = state.install_path / 'bin/perseustest'
        os.unlink(test_exe)
        os.rename(state.install_path / 'bin/perseustest_dyn', test_exe)

    @staticmethod
    def _process_pkg_config(pcfile: Path, line: str) -> str:
        return line.replace('/usr/include', '${includedir}')


class PortAudioTarget(base.CMakeDependencyTarget):
    def __init__(self, name='portaudio'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz',
            '47efbf42c77c19a05d22e627d42873e991ec0c1357219c0d74ce6a2948cb2def')

    def configure(self, state: BuildState):
        state.options['PA_BUILD_STATIC'] = 'NO'
        super().configure(state)


class RfnmAudioTarget(base.CMakeDependencyTarget):
    def __init__(self, name='rfnm'):
        super().__init__(name)
        self.prerequisites = ('spdlog',)

    def prepare_source(self, state: BuildState):
        # The following code fetches sources from the actual repository
        # The problem is, SDR++ uses own incompatible version of RFNM library
        # state.download_source(
        #     'https://github.com/rfnm/librfnm/archive/df85a47569370a3de7987b7c36d77e843ec7a41f.tar.gz',
        #     'f1bea90a6b8f66393947af5febc6cac814e87795f3fd05514e5d7928df849b86')

        state.download_source(
            'https://github.com/AlexandreRouma/librfnm/archive/4e804ec4e77b7f5f1082bafb203f5ad97d65f85a.tar.gz',
            '4067de2a96acf1710a7ce4b991bf976ac42627a545150ab6330b112a7fc8147b')


class RtAudioTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='rtaudio'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://www.music.mcgill.ca/~gary/rtaudio/release/rtaudio-6.0.1.tar.gz',
            '42d29cc2b5fa378ba3a978faeb1885a0075acf0fecb5ee50f0d76f6c7d8ab28c')

    def configure(self, state: BuildState):
        state.options['RTAUDIO_BUILD_TESTING'] = 'NO'
        super().configure(state)


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


class SDRplayTarget(base.Target):
    VERSION = '3.15.1'

    def __init__(self, name='sdrplay'):
        super().__init__(name)

    def build(self, state: BuildState):
        state.download_source(
            f'https://www.sdrplay.com/software/SDRplayAPI-macos-installer-universal-{self.VERSION}.pkg',
            '5d148ceda1fae775d2d2df5b3fcf46dee27b6222e2535c4c063c2f2ea2f7acc3')

        # Extract package payload
        pkg_suffix = '.pkgSDRplayAPI.pkg'
        pkg_dir1 = 'SDRplayAPI' + pkg_suffix
        pkg_dir2 = 'PayloadSDRplayAPI' + pkg_suffix
        payload_path = f'{pkg_dir1}/{pkg_dir2}/{pkg_dir2}/Payload'
        args = ('tar', '-xf', payload_path)
        subprocess.run(args, check=True, cwd=state.source, env=state.environment)

        # Copy headers and library to deps directory
        common_path = state.source / f'Library/SDRplayAPI/{self.VERSION}'

        for subdir in ('include', 'lib'):
            shutil.copytree(common_path / subdir, state.install_path / subdir)

        # Make .dylib symbolic link
        lib_path = state.install_path / 'lib'
        so_path = tuple(lib_path.glob('libsdrplay_api.so.*'))[0]
        os.symlink(so_path.name, lib_path / 'libsdrplay_api.dylib')


class SpdLogTarget(base.CMakeStaticDependencyTarget):
    def __init__(self, name='spdlog'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/gabime/spdlog/archive/refs/tags/v1.15.3.tar.gz',
            '15a04e69c222eb6c01094b5c7ff8a249b36bb22788d72519646fb85feb267e67')

    def configure(self, state: BuildState):
        opts = state.options
        opts['SPDLOG_BUILD_EXAMPLE'] = 'NO'
        opts['SPDLOG_BUILD_PIC'] = 'YES'

        super().configure(state)


class UsbTarget(base.ConfigureMakeSharedDependencyTarget):
    def __init__(self, name='usb'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/libusb/libusb/releases/download/v1.0.29/libusb-1.0.29.tar.bz2',
            '5977fc950f8d1395ccea9bd48c06b3f808fd3c2c961b44b0c2e6e29fc3a70a85')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('libusb/libusb.h')


class VolkTarget(base.CMakeSharedDependencyTarget):
    def __init__(self, name='volk'):
        super().__init__(name)
        self.prerequisites = ('mako', 'markupsafe')

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
