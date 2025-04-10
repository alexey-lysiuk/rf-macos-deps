#
#    Helper module to build macOS version of various radio frequency tools
#    Copyright (C) 2020-2025 Alexey Lysiuk
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
import platform
import subprocess

from ..state import BuildState
from . import base


class CMakeTarget(base.CMakeTarget):
    def __init__(self, name='cmake'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://github.com/Kitware/CMake/releases/download/v3.31.4/cmake-3.31.4.tar.gz',
            'a6130bfe75f5ba5c73e672e34359f7c0a1931521957e8393a5c2922c8b0f7f25')

    def configure(self, state: BuildState):
        # Bootstrap native CMake binary
        boostrap_path = state.native_build_path / '__bootstrap__'
        boostrap_cmk_path = boostrap_path / 'Bootstrap.cmk'
        boostrap_cmake = boostrap_cmk_path / 'cmake'

        if state.architecture() == platform.machine():
            if not boostrap_cmake.exists():
                os.makedirs(boostrap_path, exist_ok=True)

                args = (state.source / 'configure', '--parallel=' + state.jobs)
                subprocess.run(args, check=True, cwd=boostrap_path, env=state.environment)

                assert boostrap_cmake.exists()

        env = state.environment
        env['PATH'] = os.pathsep.join([str(boostrap_cmk_path), env['PATH']])

        super().configure(state)

    def post_build(self, state: BuildState):
        self.install(state)


class PkgConfigTarget(base.ConfigureMakeDependencyTarget):
    def __init__(self, name='pkg-config'):
        super().__init__(name)

    def prepare_source(self, state: BuildState):
        state.download_source(
            'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz',
            '6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591')

    def detect(self, state: BuildState) -> bool:
        return state.has_source_file('pkg-config.1')

    def post_build(self, state: BuildState):
        self.copy_to_bin(state, new_filename=self.name + '.exe')
