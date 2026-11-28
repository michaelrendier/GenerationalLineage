# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Firing plans: brackets that carry firing orders (engine/bracketing_firing_order.py, tool 4)."""
from engine import bracketing_firing_order as b


def test_verify_all_green():
    r = b.verify()
    assert r["ok"], r
    assert all(r["plans"].values()), r["plans"]


def test_two_octonion_orders_differ():
    from fractions import Fraction as F
    a = tuple(F(x) for x in (1, 2, 0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0, 1))
    p12, p21 = b.two_octonions(a, (1, 2)), b.two_octonions(a, (2, 1))
    assert b.fire_sequence(p21) == ["I", "R"]
    assert b.operator(p12) != b.operator(p21)


def test_counts():
    assert [b.count_plans(n, "nary") for n in (2, 3, 4, 5)] == [2, 14, 124, 1244]


def test_the_four_orderings_and_the_evolving_vector():
    """A bracketing, B firing order, C firing order of brackets, D bracketing of firing orders: counts, and the vector after each leaf."""
    from fractions import Fraction as F
    e = lambda k: tuple(F(int(i == k)) for i in range(16))
    ls = [b.Leaf(n, b.left_matrix(e(k)), e(k)) for n, k in zip("ABCD", (1, 2, 4, 8))]
    for n in (2, 3, 4):
        got = [len(f(ls[:n])) for f in (b.plans_bracketing, b.plans_firing_order, b.plans_firing_of_brackets, b.plans_bracketing_of_firing)]
        assert got == list(b.mode_counts(n).values())
    plan = b.parse("((A B | 2 1) C | 2 1)", {l.name: l.matrix for l in ls})
    st = b.evolve_operator(plan, e(3))
    assert [s[0] for s in st] == ["input", "C", "B", "A"] and st[-1][1] == b.apply_plan(plan, e(3))
