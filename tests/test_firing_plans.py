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
