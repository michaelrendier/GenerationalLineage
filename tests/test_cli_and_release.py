# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The command line, the package metadata, and the GPL notice on every source file."""
import glob
import os
import subprocess
import sys

import engine
from devtools.transcript import ROOT


def _run(*args):
    return subprocess.run([sys.executable, "-m", "engine", *args], cwd=ROOT, capture_output=True,
                          text=True, timeout=300, env={**os.environ, "PYTHONPATH": ROOT})


def test_cli_verify_passes():
    r = _run("--verify")
    assert r.returncode == 0, r.stdout[-600:]
    assert "RESULT: PASS" in r.stdout


def test_cli_strict_reflects_mode():
    r = _run("--verify", "--strict")
    assert r.returncode == (0 if engine.EXTENDED else 2)


def test_version_is_consistent():
    import re
    pyproject = open(os.path.join(ROOT, "pyproject.toml")).read()
    assert f'version = "{engine.__version__}"' in pyproject
    news = open(os.path.join(ROOT, "NEWS.md")).read()
    assert engine.__version__ in news


def test_star_import_works_on_any_install():
    ns = {}
    exec("from engine import *", ns)
    assert "decompose_number" in ns


def test_every_source_file_carries_the_gpl_notice():
    missing = []
    for f in glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True):
        if os.sep + ".git" + os.sep in f:
            continue
        if "SPDX-License-Identifier: GPL-3.0-only" not in open(f, encoding="utf-8").read():
            missing.append(os.path.relpath(f, ROOT))
    assert not missing, missing


def test_license_is_the_canonical_gpl3():
    text = open(os.path.join(ROOT, "LICENSE"), encoding="utf-8").read()
    assert "GNU GENERAL PUBLIC LICENSE" in text and "Version 3, 29 June 2007" in text
