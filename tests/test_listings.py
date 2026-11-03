# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The Manual's code is real: every extracted Listing is verbatim source that runs cold, and every toolset has an API sample."""
import importlib
import inspect
import os

import pytest

from devtools import build_docs
from devtools.api_samples import SAMPLES
from devtools.transcript import ROOT
from engine import lines

CASES = [(n, f, c) for n, items in build_docs.LISTINGS.items() for f, c in items]


@pytest.mark.parametrize("name,fn,call", CASES, ids=[f"{n}.{f}" for n, f, _ in CASES])
def test_listing_is_verbatim_and_runs_cold(name, fn, call):
    src, imps = build_docs.extract_listing(name, fn)
    real = importlib.import_module(lines.TOOLSETS[name]["module"])
    assert src == inspect.getsource(getattr(real, fn)).rstrip("\n"), "the Listing is not the source"
    value = build_docs.run_cold(src, imps, call)          # empty namespace: no state from anywhere else
    live = eval(call, dict(vars(real)))
    assert value == live, "the cold run and the module disagree"
    page = open(os.path.join(ROOT, "wiki", build_docs.WIKI_OF[name] + ".md"), encoding="utf-8").read()
    assert src in page, "the Listing is missing from its Manual page"


def test_every_non_extended_toolset_has_api_samples_that_run():
    for name, d in lines.TOOLSETS.items():
        if name in build_docs.ENTRY_OVERRIDE or d.get("requires"):
            continue
        assert name in SAMPLES, f"{name}: add a sample to devtools/api_samples.py"
        mod = importlib.import_module(d["module"])
        da, dk, ba, bk = SAMPLES[name]
        assert mod.descend(*da, **dk)
        try:
            assert mod.build_up(*ba, **bk)
        except lines.AscentNotFree:
            pass                                          # a refusal is a valid, documented result


def test_engine_api_page_lists_every_exported_function():
    import engine
    page = open(os.path.join(ROOT, "wiki", "Engine-API.md"), encoding="utf-8").read()
    missing = [n for n in dir(engine) if not n.startswith("_") and callable(getattr(engine, n))
               and getattr(getattr(engine, n), "__module__", "").startswith("engine") and not inspect.ismodule(getattr(engine, n))
               and f"`{n}(" not in page and f"class {n}" not in page]
    assert not missing, missing
