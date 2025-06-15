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
import plistlib
import shutil
import subprocess

from aedi.state import BuildState
from aedi.target.base import CMakeMainTarget
from aedi.utility import (
    OS_VERSION_X86_64,
    apply_unified_diff,
    hardcopy,
    hardcopy_directory,
)


class SdrPlusPlusBaseTarget(CMakeMainTarget):
    class BundleWriter:
        def __init__(self, target, state: BuildState):
            assert not state.xcode

            self.target = target
            self.state = state
            self.executable = 'sdrpp'
            self.icon = 'sdrpp.icns'

            self.build_path = state.build_path
            self.src_res_path = state.source / 'root/res'

            self.bundle_path = state.install_path / target.outputs[0]
            self.contents_path = self.bundle_path / 'Contents'
            self.plist_path = self.contents_path / 'Info.plist'
            self.macos_path = self.contents_path / 'MacOS'
            self.resources_path = self.contents_path / 'Resources'
            self.lib_path = self.contents_path / 'lib'

            self._write()

        def _write(self):
            if self.bundle_path.exists():
                shutil.rmtree(self.bundle_path)

            os.makedirs(self.macos_path)
            hardcopy_directory(self.src_res_path, self.resources_path)
            hardcopy(self.build_path / self.executable, self.macos_path / self.executable)

            self._write_libs()
            self._write_plist()
            self._write_icon()

        def _write_libs(self):
            core_lib = 'libsdrpp_core.dylib'
            os.mkdir(self.lib_path)
            hardcopy(self.build_path / 'core' / core_lib, self.lib_path / core_lib)

            for dependency in self.target.dependencies:
                dylib = f'lib{dependency}.dylib'
                hardcopy(self.state.lib_path / dylib, self.lib_path / dylib)

            plugins_path = self.contents_path / 'Plugins'
            os.mkdir(plugins_path)

            for module in self.build_path.glob('**/*.dylib'):
                if module.name != core_lib:
                    hardcopy(module, plugins_path / module.name)

        def _write_plist(self):
            version = self.state.source_version().strip()
            plist = {
                'CFBundleExecutable': self.executable,
                'CFBundleIconFile': self.icon,
                'CFBundleIdentifier': 'org.sdrpp.sdrpp',
                'CFBundleInfoDictionaryVersion': '6.0',
                'CFBundleName': 'SDR++',
                'CFBundlePackageType': 'APPL',
                'CFBundleShortVersionString': version,
                'CFBundleVersion': version,
                'LSMinimumSystemVersion': str(OS_VERSION_X86_64),
                'NSHighResolutionCapable': True,
                'NSSupportsAutomaticGraphicsSwitching': True,
            }

            with open(self.plist_path, 'wb') as f:
                plistlib.dump(plist, f)

        def _write_icon(self):
            iconset_path = self.build_path / 'sdrpp.iconset'

            if iconset_path.exists():
                shutil.rmtree(iconset_path)

            os.mkdir(iconset_path)

            icon_path = self.src_res_path / 'icons/sdrpp.macos.png'
            resolutions = (16, 32, 64, 128, 256, 512)

            for resolution in resolutions:
                res_str = str(resolution)
                args = (
                    '/usr/bin/sips',
                    '--resampleHeightWidth', res_str, res_str,
                    icon_path,
                    '--out', iconset_path / f'icon_{resolution}x{resolution}.png',
                )
                subprocess.run(args, check=True, env=self.state.environment, stdout=subprocess.DEVNULL)

            args = (
                '/usr/bin/iconutil',
                '-c', 'icns',
                iconset_path,
                '-o', self.resources_path / self.icon
            )
            subprocess.run(args, check=True, env=self.state.environment)

    def __init__(self, name=None):
        super().__init__(name)
        self.outputs = ('SDR++.app',)
        self.dependencies = [
            'ad9361.0',
            'airspy.0',
            'airspyhf.0',
            'bladeRF.2',
            'fftw3f.3.6.9',
            'fobos',
            'glfw.3',
            'hackrf.0',
            'iio.0',
            'LimeSuite.23.11-1',
            'perseus-sdr.0',
            'portaudio',
            'rfnm',
            'rtaudio.7',
            'rtlsdr.0',
            'usb-1.0.0',
            'volk.3.2',
            'zstd.1'
        ]

    def configure(self, state: BuildState):
        opts = state.options
        opts['OPT_BUILD_AUDIO_SINK'] = 'NO'
        opts['USE_BUNDLE_DEFAULTS'] = 'YES'
        opts['USE_INTERNAL_LIBCORRECT'] = 'NO'

        enabled_options = (
            'BLADERF_SOURCE',
            'FOBOSSDR_SOURCE',
            'LIMESDR_SOURCE',
            'M17_DECODER',
            'NEW_PORTAUDIO_SINK',
            'PERSEUS_SOURCE',
            'PORTAUDIO_SINK',
            'RFNM_SOURCE',
            'SDRPLAY_SOURCE',
        )

        for option in enabled_options:
            opts['OPT_BUILD_' + option] = 'YES'

        super().configure(state)

    def post_build(self, state: BuildState):
        if state.xcode:
            self._prepare_xcode(state)
        else:
            self.BundleWriter(self, state)

    def _prepare_xcode(self, state: BuildState):
        assert state.xcode

        # Shared library dependencies
        CMakeMainTarget.hardcopy_xcode_deps(state, *self.dependencies)

        # SDR++ modules
        plugins_path = state.build_path / 'Plugins'
        plugins_path.mkdir(parents=True, exist_ok=True)

        for modules_path in state.build_path.glob('*_modules'):
            for module_path in modules_path.iterdir():
                if module_path.is_dir():
                    module_dylib = f'{module_path.name}.dylib'
                    module_dest = plugins_path / module_dylib

                    # Check for symlink existence regardless of target file presence
                    # pathlib.Path.exists() returns True only when symlink points to existing file
                    if not module_dest.is_symlink():
                        module_dest.symlink_to(module_path / 'Debug' / module_dylib)

        # SDR++ resources
        resources_path = state.build_path / 'Resources'

        if not resources_path.exists():
            resources_path.symlink_to(state.source / 'root/res')


class SdrPlusPlusTarget(SdrPlusPlusBaseTarget):
    def __init__(self):
        super().__init__('sdrpp')

    def prepare_source(self, state: BuildState):
        state.checkout_git('https://github.com/AlexandreRouma/SDRPlusPlus.git')

    def configure(self, state: BuildState):
        apply_unified_diff(state.patch_path / 'sdrpp-local-ad9361-iio.diff', state.source)
        super().configure(state)


class SrdppExpTarget(SdrPlusPlusBaseTarget):
    def __init__(self):
        super().__init__('sdrpp-exp')
        self.dependencies.append('libfobos_sdr')

    def prepare_source(self, state: BuildState):
        state.checkout_git('https://github.com/alexey-lysiuk/sdrpp-exp.git')

    def configure(self, state: BuildState):
        state.options['OPT_BUILD_DISCORD_PRESENCE'] = 'NO'
        state.options['OPT_BUILD_FOBOSSDR_AGILE_SOURCE'] = 'YES'
        super().configure(state)
