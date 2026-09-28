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
devtools/transcript.py — turn a runnable example script into a REPL transcript.

    python3 devtools/transcript.py examples/11_periodicity.py            # print
    python3 devtools/transcript.py --write-all                          # regenerate examples/transcripts/
    python3 devtools/transcript.py --check-all                          # fail if any committed transcript is stale

Convention D (a literal session at a live evaluator): every top-level statement of the
script is shown after a `>>> ` prompt (`... ` for continuation lines), then executed in one
shared namespace, and whatever it prints — or, for a bare expression, its repr — is echoed
exactly as the interpreter would. Nothing is retyped: the transcript IS the output of the
script, so it cannot drift from what the code does.

The module docstring is the title/abstract and is not part of the transcript. Comment lines
sitting directly above a statement are shown with it.
"""
import ast
import contextlib
import io
import os
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def transcript(path: str) -> str:
    src = open(path, encoding="utf-8").read()
    lines = src.split("\n")
    tree = ast.parse(src, filename=path)
    body = list(tree.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]                                    # the docstring is the title
    ns = {"__name__": "__main__", "__file__": path}
    old_cwd, old_path = os.getcwd(), list(sys.path)
    os.chdir(ROOT)
    sys.path.insert(0, ROOT)
    out = []
    prev_end = 0
    try:
        for node in body:
            start = node.lineno
            # pull in comment lines directly above (no blank line between)
            s = start - 1
            while s - 1 >= prev_end and lines[s - 1].lstrip().startswith("#"):
                s -= 1
            seg = lines[s:node.end_lineno]
            prev_end = node.end_lineno
            n_comment = start - 1 - s          # comment lines above the statement: each its own prompt
            for i, ln in enumerate(seg):
                if i <= n_comment:
                    out.append(">>> " + ln)
                else:
                    out.append((">>> " if i == n_comment else "... ") + ln if ln.strip() else "...")
            buf = io.StringIO()
            # 'single' is the REPL's own compile mode: a bare expression anywhere in the
            # statement (even inside try/for) echoes its repr, exactly as at a prompt.
            code = compile("\n".join(lines[start - 1:node.end_lineno]) + "\n", path, "single")
            with contextlib.redirect_stdout(buf):
                exec(code, ns)
            text = buf.getvalue()
            if text:
                out.extend(text.rstrip("\n").split("\n"))
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path
    return "\n".join(out) + "\n"


def all_examples():
    return sorted(glob.glob(os.path.join(ROOT, "examples", "[0-9][0-9]_*.py")))


def needs_extended(example: str) -> bool:
    """Tutorials numbered 9x exercise the EXTENDED layer; their committed transcript was made with it."""
    return os.path.basename(example).startswith("9")


def _extended_available() -> bool:
    sys.path.insert(0, ROOT)
    import engine
    return engine.EXTENDED


def transcript_path(example: str) -> str:
    return os.path.join(ROOT, "examples", "transcripts",
                        os.path.splitext(os.path.basename(example))[0] + ".txt")


def main(argv):
    if "--write-all" in argv:
        ext = _extended_available()
        for ex in all_examples():
            if needs_extended(ex) and not ext:
                print("kept   ", os.path.relpath(transcript_path(ex), ROOT), "(EXTENDED layer not installed — not regenerated)")
                continue
            t = transcript(ex)
            with open(transcript_path(ex), "w", encoding="utf-8") as f:
                f.write(t)
            print("wrote", os.path.relpath(transcript_path(ex), ROOT), f"({t.count(chr(10))} lines)")
        return 0
    if "--check-all" in argv:
        stale, skipped = [], []
        ext = _extended_available()
        for ex in all_examples():
            if needs_extended(ex) and not ext:
                skipped.append(os.path.relpath(ex, ROOT))
                continue
            tp = transcript_path(ex)
            if not os.path.exists(tp) or open(tp, encoding="utf-8").read() != transcript(ex):
                stale.append(os.path.relpath(ex, ROOT))
        print("stale transcripts:", stale or "none", ("| skipped (EXTENDED layer not installed): %s" % skipped) if skipped else "")
        return 1 if stale else 0
    if len(argv) >= 1 and not argv[0].startswith("-"):
        sys.stdout.write(transcript(argv[0]))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
