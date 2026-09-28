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
python3 -m engine            what is installed, and in which mode (CORE / EXTENDED)
python3 -m engine --verify   run every toolset's self-check; exit 0 iff all that ran passed
python3 -m engine --verify --strict   also fail if any toolset was skipped
python3 -m engine --lines    print the two lines (what is free, what is paid)
python3 -m engine --list     list the registered toolsets

CORE      the whole engine except the Fermat-facet layer; needs only numpy.
EXTENDED  CORE plus engine.maths / engine.tools / engine.oscilloscope, which reach
          four sibling repos (see README, 'Extended install').
"""
import argparse
import platform
import sys


def _banner() -> None:
    import engine
    try:
        import numpy
        npv = numpy.__version__
    except ImportError:                                            # pragma: no cover
        npv = "NOT INSTALLED (required)"
    mode = "EXTENDED" if engine.EXTENDED else "CORE"
    print(f"GenerationalLineage {engine.__version__}  ·  mode: {mode}")
    print(f"python {platform.python_version()}  ·  numpy {npv}")
    if not engine.EXTENDED:
        print(f"extended layer absent: {engine.IMPORT_ERROR!r}")
        print("  (expected on a plain clone — see README, 'Extended install')")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m engine", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true", help="run every toolset's self-check")
    ap.add_argument("--strict", action="store_true", help="with --verify: fail if anything was skipped")
    ap.add_argument("--lines", action="store_true", help="print the two lines")
    ap.add_argument("--list", action="store_true", help="list the registered toolsets")
    a = ap.parse_args(argv)

    _banner()
    from engine import lines

    if a.list:
        print()
        for n, d in lines.TOOLSETS.items():
            print(f"  {n:<18} line={d['line']:<13}{'  [extended]' if d.get('requires') else ''}")
    if a.lines:
        print()
        print(lines.describe_lines())
    if a.verify:
        print()
        v = lines.verify_all()
        for k, r in v.items():
            if k.startswith("_"):
                continue
            if r.get("skipped"):
                print(f"  SKIP  {k}   {r['reason']}")
            elif r.get("ok"):
                print(f"  ok    {k}")
            else:
                print(f"  FAIL  {k}   {r}")
        n_ran = sum(1 for k, r in v.items() if not k.startswith("_") and not r.get("skipped"))
        print(f"\n{n_ran} toolsets ran, "
              f"{sum(1 for k, r in v.items() if not k.startswith('_') and r.get('ok'))} passed, "
              f"{len(v['_skipped'])} skipped")
        if not v["_ok"]:
            print("RESULT: FAIL")
            return 1
        if a.strict and not v["_complete"]:
            print("RESULT: INCOMPLETE (strict) — skipped: " + ", ".join(v["_skipped"]))
            return 2
        print("RESULT: PASS" + ("" if v["_complete"] else "  (core; extended layer skipped)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
