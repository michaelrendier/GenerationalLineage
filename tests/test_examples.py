# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Every tutorial runs standalone, and its committed transcript is exactly what the code prints today."""
import os
import subprocess
import sys

import pytest

import engine
from devtools import transcript as T   # devtools/ is importable from the repo root

ROOT = T.ROOT
EXAMPLES = T.all_examples()


def _needs_extended(path):
    return T.needs_extended(path)


@pytest.mark.parametrize("path", EXAMPLES, ids=[os.path.basename(p) for p in EXAMPLES])
def test_example_runs_standalone(path):
    r = subprocess.run([sys.executable, path], cwd=ROOT, capture_output=True, text=True, timeout=300,
                       env={**os.environ, "PYTHONPATH": ROOT})
    assert r.returncode == 0, r.stderr[-800:]


@pytest.mark.parametrize("path", EXAMPLES, ids=[os.path.basename(p) for p in EXAMPLES])
def test_transcript_is_not_stale(path):
    if _needs_extended(path) and not engine.EXTENDED:
        pytest.skip("EXTENDED-layer tutorial")
    tp = T.transcript_path(path)
    assert os.path.exists(tp), "missing transcript — run: python3 devtools/transcript.py --write-all"
    assert open(tp, encoding="utf-8").read() == T.transcript(path), "stale — run: python3 devtools/transcript.py --write-all"
