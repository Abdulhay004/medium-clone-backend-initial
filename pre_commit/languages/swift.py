from __future__ import annotations

import contextlib
import os
from collections.abc import Generator
from collections.abc import Sequence

from pre_commit import lang_base
from pre_commit.envcontext import envcontext
from pre_commit.envcontext import PatchesT
from pre_commit.envcontext import Var
from pre_commit.prefix import Prefix
from pre_commit.util import cmd_output_b

BUILD_DIR = '.build'
BUILD_CONFIG = 'release'

ENVIRONMENT_DIR = 'swift_env'
get_default_version = lang_base.basic_get_default_version
health_check = lang_base.basic_health_check
run_hook = lang_base.basic_run_hook


def get_env_patch(venv: str) -> PatchesT:  # pragma: win32 no cover
    bin_path = os.path.join(venv, BUILD_DIR, BUILD_CONFIG)
    return (('PATH', (bin_path, os.pathsep, Var('PATH'))),)


@contextlib.contextmanager  # pragma: win32 no cover
def in_env(prefix: Prefix, version: str) -> Generator[None, None, None]:
    envdir = lang_base.environment_dir(prefix, ENVIRONMENT_DIR, version)
    with envcontext(get_env_patch(envdir)):
        yield


def install_environment(
        prefix: Prefix, version: str, additional_dependencies: Sequence[str],
) -> None:  # pragma: win32 no cover
    lang_base.assert_version_default('swift', version)
    lang_base.assert_no_additional_deps('swift', additional_dependencies)
    envdir = lang_base.environment_dir(prefix, ENVIRONMENT_DIR, version)

    # Build the swift package
    os.mkdir(envdir)
    cmd_output_b(
        'swift', 'build',
        '--package-path', prefix.prefix_dir,
        '-c', BUILD_CONFIG,
        '--build-path', os.path.join(envdir, BUILD_DIR),
    )
