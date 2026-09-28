# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Every registered toolset checks itself; the contract holds for all of them."""
import importlib

import pytest

from engine import lines

NEW_TEN = ["periodicity", "lyndon", "berlekamp_massey", "logperiodic", "permutation",
           "rejewski", "jordan_chevalley", "re_pair", "pohlig_hellman", "unicity"]


@pytest.fixture(scope="module")
def verified():
    return lines.verify_all()


@pytest.mark.parametrize("name", list(lines.TOOLSETS))
def test_toolset_self_check(name, verified):
    r = verified[name]
    if r.get("skipped"):
        pytest.skip(r["reason"])          # EXTENDED-layer toolset on a CORE install
    assert r["ok"] is True, r


def test_verify_all_reports_honestly(verified):
    assert verified["_ok"] is True
    assert verified["_complete"] == (not verified["_skipped"])


@pytest.mark.parametrize("name", [n for n in lines.TOOLSETS if lines.TOOLSETS[n].get("module", "").startswith("engine.toolsets.")])
def test_toolset_contract(name):
    m = importlib.import_module(lines.TOOLSETS[name]["module"])
    assert m.NAME == name
    assert m.LINE in ("decomposition", "emerger", "both")
    for fn in ("descend", "build_up", "verify"):
        assert callable(getattr(m, fn)), f"{name} lacks {fn}()"


@pytest.mark.parametrize("name", NEW_TEN)
def test_ascent_refuses_when_owed_something(name):
    """The refusal IS the result: an empty target is not silently guessed at."""
    with pytest.raises(lines.AscentNotFree) as e:
        lines.build_up(name, {})
    assert e.value.owed


def test_dispatcher_forwards_two_argument_descents():
    assert lines.descend("stencil", 53, 61)["N"] == 3233
    assert lines.descend("hyper_linear", 12, 34)["product"] == 408
    r = lines.descend("scale", 15.0, reference=3.0)
    assert r["free"] is True and r["cost"] == 0
