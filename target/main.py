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
from aedi.utility import apply_unified_diff


class SdrPlusPlusTarget(CMakeMainTarget):
    def __init__(self, name='sdrpp'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.checkout_git('https://github.com/AlexandreRouma/SDRPlusPlus.git')

    def configure(self, state: BuildState):
        apply_unified_diff(state.patch_path / 'sdrpp-no-frameworks.diff', state.source)

        opts = state.options
        build_options = {
            'AIRSPY_SOURCE': 'NO',
            'AIRSPYHF_SOURCE': 'NO',
            'AUDIO_SINK': 'NO',
            'DISCORD_PRESENCE': 'NO',
            'FOBOSSDR_SOURCE': 'YES',
            'FOBOSSDR_AGILE_SOURCE': 'YES',
            'NEW_PORTAUDIO_SINK': 'YES',
            'PORTAUDIO_SINK': 'YES',
        }

        for name, value in build_options.items():
            opts['OPT_BUILD_' + name] = value

        opts['USE_BUNDLE_DEFAULTS'] = 'YES'
        opts['USE_INTERNAL_LIBCORRECT'] = 'NO'

        super().configure(state)

    def post_build(self, state: BuildState):
        if state.xcode:
            self._post_build_xcode(state)

        super().post_build(state)

    def _post_build_xcode(self, state: BuildState):
        assert state.xcode

        # Shared library dependencies
        self.hardcopy_xcode_deps(state, 'ad9361', 'fftw3f', 'fobos', 'fobos_sdr', 'glfw',
            'hackrf', 'iio', 'portaudio', 'rtaudio', 'rtlsdr', 'usb', 'volk', 'zstd')

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
