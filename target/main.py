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

from aedi.state import BuildState
from aedi.target.base import CMakeMainTarget
from aedi.utility import hardlink_directories


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

        opts['OPT_BUILD_FOBOSSDR_SOURCE'] = 'YES'
        opts['USE_BUNDLE_DEFAULTS'] = 'YES'
        opts['USE_INTERNAL_LIBCORRECT'] = 'NO'

        super().configure(state)

    def post_build(self, state: BuildState):
        if state.xcode:
            config = 'Debug'

            # Shared library dependencies
            hardlink_directories((state.lib_path,), state.build_path / config, cleanup=False)

            # SDR++ modules
            plugins_path = state.build_path / 'Plugins'
            os.makedirs(plugins_path, exist_ok=True)

            for modules_path in state.build_path.glob('*_modules'):
                for module_path in modules_path.iterdir():
                    if module_path.is_dir():
                        module_dylib = f'{module_path.name}.dylib'
                        module_dest = plugins_path / module_dylib

                        # Check for symlink existence regardless of target file presence
                        # pathlib.Path.exists() returns True only when symlink points to existing file
                        if not module_dest.is_symlink():
                            os.symlink(module_path / config / module_dylib, module_dest)

            # SDR++ resources
            resources_path = state.build_path / 'Resources'

            if not resources_path.exists():
                os.symlink(state.source / 'root/res', resources_path)

        super().post_build(state)
