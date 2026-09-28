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


def test_every_python_block_in_the_readme_runs(tmp_path, monkeypatch):
    """The README's code is held to the same bar as the tutorials: each block is complete and runnable.
    Blocks tagged [EXTENDED ...] need the sibling repositories (and matplotlib, for the two chart writers)."""
    import re
    text = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    text = re.sub(r"<!-- BEGIN: (\w[\w-]*).*?<!-- END: \1 -->", "", text, flags=re.S)   # generated blocks have their own tests
    blocks = re.findall(r"```python\n(.*?)```", text, re.S)
    assert len(blocks) >= 20, "the README lost its code blocks?"
    try:
        import matplotlib
        matplotlib.use("Agg")
        have_mpl = True
    except ImportError:
        have_mpl = False
    monkeypatch.chdir(tmp_path)                     # chart writers drop PNGs here, not in the repository
    ran = 0
    for i, b in enumerate(blocks):
        if b.lstrip().startswith("# [EXTENDED") and not (engine.EXTENDED and have_mpl):
            continue
        try:
            exec(compile(b, f"<README python block {i}>", "exec"), {})
        except Exception as e:                      # noqa: BLE001
            raise AssertionError(f"README python block {i} failed: {type(e).__name__}: {e}\n---\n{b[:400]}") from e
        ran += 1
    assert ran >= 18


def _github_slug(heading: str) -> str:
    """GitHub's heading-anchor rule: lowercase; drop everything but letters, digits, spaces, hyphens, underscores; spaces -> hyphens."""
    import re
    h = heading.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h, flags=re.UNICODE)
    return h.replace(" ", "-")


def test_readme_internal_links_and_relative_paths_resolve():
    """Every #anchor in the README points at a real heading; every relative link in the README and wiki points at a real file."""
    import re
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    in_fence, slugs, seen = False, set(), {}
    for line in readme.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        m = re.match(r"^#{1,6} (.+)$", line)
        if m and not in_fence:
            slug = _github_slug(m.group(1).replace("`", ""))
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            slugs.add(slug if n == 0 else f"{slug}-{n}")
    bad_anchor = [a for a in re.findall(r"\]\(#([^)]+)\)", readme) if a not in slugs]
    assert not bad_anchor, f"README anchors with no heading: {bad_anchor}"

    bad_path = []
    for md in ["README.md"] + [os.path.join("wiki", f) for f in os.listdir(os.path.join(ROOT, "wiki")) if f.endswith(".md")]:
        base = os.path.dirname(os.path.join(ROOT, md))
        txt = open(os.path.join(ROOT, md), encoding="utf-8").read()
        txt = re.sub(r"```.*?```", "", txt, flags=re.S)                       # not the code blocks
        for target in re.findall(r"\]\(([^)\s]+)\)", txt):
            if target.startswith(("http://", "https://", "mailto:", "#")) or not re.search(r"[./]", target):
                continue                                        # a URL, an anchor, or maths like M[f](s)
            path = target.split("#")[0]
            if path and not os.path.exists(os.path.normpath(os.path.join(base, path))):
                bad_path.append((md, target))
    assert not bad_path, f"relative links to files that do not exist: {bad_path[:10]}"
