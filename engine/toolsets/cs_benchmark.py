# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
#
# GenerationalLineage is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# GenerationalLineage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only
"""
GenerationalLineage.engine.toolsets.cs_benchmark
==================================================
CS_BENCHMARK -- measure a callable's real cost, once, honestly. Citation
travels in the code: every result this toolset returns carries `CITATION`
as a data field, not a separate footnote a caller has to remember to keep
attached.

Methodology source: Patterson, Gonzalez, Le, Liang, Munguia, Rothchild, So,
Texier, Dean (2021), "Carbon Emissions and Large Neural Network Training",
arXiv:2104.10350 -- their own footprint identity is

    Footprint = (energy_train + queries * energy_inference) * CO2e_per_KWh

cited here for the discipline it argues for: report the actual measured
cost of a real run, on real hardware, as a first-class transparent number
-- not a theoretical FLOP estimate, not an afterthought. `footprint()`
below is that formula, directly.

DECOMPOSITION (free): `descend` -- benchmark ONE callable, one measurement
pass, no search. The honest, minimal reading.

EMERGER (work): `build_up` -- benchmark several CANDIDATE callables against
a shared reference cost and rank them. Searching for the cheapest
candidate is the work; reading one candidate's own cost is not.
"""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

NAME = "cs_benchmark"
LINE = "both"

CITATION = ("Patterson et al. (2021), \"Carbon Emissions and Large Neural "
            "Network Training\", arXiv:2104.10350")


def _time_calls(fn: Callable, args: Tuple, kwargs: Dict, n: int) -> float:
    """Total wall-clock seconds for n calls. No warmup hidden -- the first
    call counts, the same way a real cold read would pay for it."""
    t0 = time.perf_counter()
    for _ in range(n):
        fn(*args, **kwargs)
    return time.perf_counter() - t0


def descend(fn: Callable, args: Tuple = (), kwargs: Optional[Dict] = None,
            n: int = 1000) -> Dict[str, Any]:
    """The FREE reading: benchmark ONE callable, directly, n calls, no
    comparison and no search. Returns real measured seconds/call and
    calls/sec -- the honest minimum a cost claim needs."""
    kwargs = kwargs or {}
    total_s = _time_calls(fn, args, kwargs, n)
    per_call = total_s / n if n else float("nan")
    return {
        "toolset": NAME, "n_calls": n, "total_s": total_s,
        "s_per_call": per_call,
        "calls_per_s": (1.0 / per_call) if per_call > 0 else float("inf"),
        "citation": CITATION,
        "note": "one measurement pass, real wall-clock time -- the free reading",
    }


def build_up(candidates: Dict[str, Callable], reference_s_per_call: float,
             args: Tuple = (), kwargs: Optional[Dict] = None,
             n: int = 1000) -> Dict[str, Any]:
    """The WORK: benchmark every candidate in `candidates`, rank them
    against a shared `reference_s_per_call` (e.g. a known baseline cost),
    report each one's speedup. `cost` = candidates scanned."""
    kwargs = kwargs or {}
    results: List[Dict[str, Any]] = []
    for name, fn in candidates.items():
        r = descend(fn, args=args, kwargs=kwargs, n=n)
        speedup = (reference_s_per_call / r["s_per_call"]
                   if r["s_per_call"] > 0 else float("inf"))
        results.append({"name": name, "s_per_call": r["s_per_call"],
                         "speedup_vs_reference": speedup})
    results.sort(key=lambda r: r["s_per_call"])
    return {
        "toolset": NAME, "n_candidates": len(candidates),
        "reference_s_per_call": reference_s_per_call,
        "ranked": results, "fastest": results[0]["name"] if results else None,
        "cost": len(candidates), "citation": CITATION,
        "note": "ranked by measured cost against the shared reference",
    }


def footprint(energy_train_kwh: float, n_queries: int,
              energy_inference_kwh: float,
              co2e_per_kwh: Optional[float] = None) -> Dict[str, Any]:
    """Patterson et al.'s own footprint identity, directly:
    Footprint = (energy_train + queries * energy_inference) * CO2e_per_KWh.
    `co2e_per_kwh` is optional -- omit it to get the raw energy total
    (kWh) without a carbon-intensity conversion; supply it (their own
    Table 2 gives real per-datacentre values) to get tCO2e."""
    energy_kwh = energy_train_kwh + n_queries * energy_inference_kwh
    out = {
        "toolset": NAME, "energy_train_kwh": energy_train_kwh,
        "n_queries": n_queries, "energy_inference_kwh": energy_inference_kwh,
        "energy_total_kwh": energy_kwh, "citation": CITATION,
    }
    if co2e_per_kwh is not None:
        out["co2e_per_kwh"] = co2e_per_kwh
        out["footprint_co2e"] = energy_kwh * co2e_per_kwh
    return out


def verify() -> Dict[str, Any]:
    def fast(x):
        return x + 1

    def slow(x):
        s = 0
        for _ in range(200):
            s += x
        return s

    d = descend(fast, args=(1,), n=2000)
    ok_descend = d["s_per_call"] >= 0.0 and d["calls_per_s"] > 0 and \
        d["citation"] == CITATION

    b = build_up({"fast": fast, "slow": slow},
                 reference_s_per_call=1.0, args=(1,), n=500)
    ok_build_up = (b["fastest"] == "fast" and b["cost"] == 2 and
                   b["ranked"][0]["s_per_call"] <= b["ranked"][1]["s_per_call"])

    f = footprint(energy_train_kwh=100.0, n_queries=1000,
                  energy_inference_kwh=0.001, co2e_per_kwh=0.4)
    ok_footprint = (abs(f["energy_total_kwh"] - 101.0) < 1e-9 and
                    abs(f["footprint_co2e"] - 40.4) < 1e-9)

    return {"ok": ok_descend and ok_build_up and ok_footprint,
            "descend": ok_descend, "build_up": ok_build_up,
            "footprint": ok_footprint}


if __name__ == "__main__":
    print(descend(lambda x: x * x, args=(7,), n=5000))
    print(footprint(energy_train_kwh=1287.0, n_queries=1, energy_inference_kwh=0.0,
                     co2e_per_kwh=0.429))
    print(verify())
