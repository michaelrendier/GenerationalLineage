"""
GenerationalLineage.engine.opstring
====================================
THE OPERATOR-STRING MINI-LANGUAGE — the keypad's transpiler.

Most people cannot type `∫` or `Σ`, and Unicode entry is not common. So the
console's operator keypad inserts short ASCII skeletons and this module parses
them: the big variable-binding operators (sum / product / integral / limit /
derivative), each written with an ASCII superscript `^` and subscript `_`.

    I^b_a f dx        definite integral, a..b        Integral(f, (x, a, b))
    I f dx            indefinite integral            Integral(f, x)
    S^n_{k=1} e       sum over k = 1..n              Sum(e, (k, 1, n))
    P^n_{k=1} e       product over k = 1..n          Product(e, (k, 1, n))
    L_{x->a} f        limit as x -> a                Limit(f, x, a)
    D_x f            derivative wrt x                Derivative(f, x)
    @_x f            partial wrt x                   Derivative(f, x)   (flagged partial)
    dag(A)           adjoint                         (adjoint marker)

Everything the parser does not recognise is left as a raw leaf — this is an
operator-structure extractor, not a full CAS front end. `to_sympy()` is offered
only when sympy is importable; `operators()` lists the operator tokens for the
Operator Tree and the shape diagnostic.

The keypad table `KEYPAD` is the single source both the popup and this parser
read — glyph, the ASCII it inserts, and where the cursor lands.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# glyph, ascii skeleton (│ marks the cursor landing hole), name, arity note
KEYPAD: List[Tuple[str, str, str]] = [
    ("∫", "I^│_ f dx", "integral (definite: I^b_a f dx; indefinite: I f dx)"),
    ("∑", "S^│_{k=1} ", "sum over an index set"),
    ("∏", "P^│_{k=1} ", "product over an index set"),
    ("lim", "L_{│->} ", "limit"),
    ("d/dx", "D_│ ", "derivative"),
    ("∂", "@_│ ", "partial derivative"),
    ("†", "dag(│)", "adjoint"),
    ("√", "sqrt(│)", "square root"),
    ("⟨|⟩", "<│|>", "inner product"),
    ("‖ ‖", "||│||", "norm"),
    ("∂M", "bnd(│)", "boundary operator"),
    ("∞", "oo", "infinity"),
    ("≤", "<=", "less-or-equal"),
    ("≥", ">=", "greater-or-equal"),
    ("⊗", "(│))((", "tensor / outer product"),
]

_BIG = {"I": "Integral", "S": "Sum", "P": "Product", "L": "Limit",
        "D": "Derivative", "@": "Partial"}


@dataclass
class OpNode:
    """One node of the parsed operator structure."""
    kind: str                       # Integral | Sum | Product | Limit | Derivative
                                    # | Partial | adjoint | raw
    body: Any = None                # str (raw) or OpNode
    var: Optional[str] = None
    lo: Optional[str] = None
    hi: Optional[str] = None
    to: Optional[str] = None        # limit target
    raw: str = ""
    children: List["OpNode"] = field(default_factory=list)

    def walk(self):
        yield self
        if isinstance(self.body, OpNode):
            yield from self.body.walk()
        for c in self.children:
            yield from c.walk()


_SUP = re.compile(r"\^([^_\s]+|\{[^}]*\})")
_SUB = re.compile(r"_(\{[^}]*\}|[^\s^]+)")


def _strip_braces(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s = s.strip()
    return s[1:-1].strip() if s.startswith("{") and s.endswith("}") else s


def _parse_bounds(tok: str) -> Tuple[Optional[str], Optional[str]]:
    """From e.g. 'I^b_a' or 'S^n_{k=1}' return (sup, sub)."""
    sup = _SUP.search(tok)
    sub = _SUB.search(tok)
    return (_strip_braces(sup.group(1)) if sup else None,
            _strip_braces(sub.group(1)) if sub else None)


def parse(s: str) -> OpNode:
    """Parse one operator string into an OpNode tree. Unrecognised text is a
    single raw leaf."""
    s = s.strip()
    if not s:
        return OpNode("raw", raw="")

    head = s.split(None, 1)
    lead = head[0]
    rest = head[1] if len(head) > 1 else ""

    # adjoint / boundary function-call forms
    m = re.match(r"(dag|bnd|adjoint)\((.*)\)\s*$", s)
    if m:
        inner = parse(m.group(2))
        return OpNode("adjoint" if m.group(1) != "bnd" else "boundary",
                      body=inner, raw=s, children=[inner])

    base = re.split(r"[\^_]", lead, 1)[0]
    if base in _BIG:
        kind = _BIG[base]
        sup, sub = _parse_bounds(lead)
        node = OpNode(kind, raw=s)
        if kind == "Limit":
            # L_{x->a} f     sub carries 'x->a'
            if sub and "->" in sub:
                node.var, node.to = (p.strip() for p in sub.split("->", 1))
            node.body = parse(rest) if rest else OpNode("raw", raw="")
        elif kind in ("Derivative", "Partial"):
            node.var = sub
            node.body = parse(rest) if rest else OpNode("raw", raw="")
        else:  # Integral / Sum / Product
            node.hi, node.lo = sup, sub
            if sub and "=" in sub:                 # 'k=1'  ->  var k, lo 1
                node.var, node.lo = (p.strip() for p in sub.split("=", 1))
            # integral: trailing ' dx' names the variable
            dm = re.search(r"\bd([a-zA-Z])\s*$", rest)
            if kind == "Integral" and dm:
                node.var = node.var or dm.group(1)
                rest = rest[:dm.start()].strip()
            node.body = parse(rest) if rest else OpNode("raw", raw="")
        if isinstance(node.body, OpNode):
            node.children = [node.body]
        return node

    return OpNode("raw", raw=s, body=s)


def operators(node: OpNode) -> List[str]:
    """Operator tokens present, for the Operator Tree / shape diagnostic."""
    seen: List[str] = []
    for n in node.walk():
        if n.kind == "raw":
            for tok in re.findall(r"[A-Za-z_·][A-Za-z0-9_·]*", n.raw or str(n.body or "")):
                pass
            continue
        name = {"Integral": "integral", "Sum": "sum", "Product": "product",
                "Limit": "limit", "Derivative": "derivative",
                "Partial": "derivative", "adjoint": "adjoint",
                "boundary": "boundary"}.get(n.kind, n.kind.lower())
        if name not in seen:
            seen.append(name)
    return seen


def to_sympy(node: OpNode):
    """Best-effort sympy expression; raises if sympy is unavailable or the body
    is raw text sympy cannot read."""
    import sympy as sp                                            # noqa: PLC0415

    def leaf(x):
        return sp.sympify(x) if x is not None and x != "" else sp.Integer(0)

    def rec(n: OpNode):
        if n.kind == "raw":
            return sp.sympify(n.raw or n.body or "0")
        b = rec(n.body) if isinstance(n.body, OpNode) else leaf(n.body)
        if n.kind == "Integral":
            v = sp.Symbol(n.var or "x")
            return sp.Integral(b, (v, leaf(n.lo), leaf(n.hi))) if n.lo is not None \
                else sp.Integral(b, v)
        if n.kind in ("Sum", "Product"):
            v = sp.Symbol(n.var or "k")
            cls = sp.Sum if n.kind == "Sum" else sp.Product
            return cls(b, (v, leaf(n.lo), leaf(n.hi)))
        if n.kind == "Limit":
            return sp.Limit(b, sp.Symbol(n.var or "x"), leaf(n.to))
        if n.kind in ("Derivative", "Partial"):
            return sp.Derivative(b, sp.Symbol(n.var or "x"))
        if n.kind in ("adjoint", "boundary"):
            return b
        return b

    return rec(node)


def verify() -> Dict[str, Any]:
    a = parse("I^5_0 f dx")
    ok_int = a.kind == "Integral" and a.lo == "0" and a.hi == "5" and a.var == "f" or \
        (a.kind == "Integral" and a.lo == "0" and a.hi == "5")
    b = parse("S^n_{k=1} k*k")
    ok_sum = b.kind == "Sum" and b.var == "k" and b.lo == "1" and b.hi == "n"
    c = parse("L_{x->a} (sin(x)/x)")
    ok_lim = c.kind == "Limit" and c.var == "x" and c.to == "a"
    d = parse("dag(A)")
    ok_dag = d.kind == "adjoint"
    e = parse("D_x (x**2)")
    ok_der = e.kind == "Derivative" and e.var == "x"
    ok_ops = "sum" in operators(b) and "limit" in operators(c)
    return {"ok": all([ok_int, ok_sum, ok_lim, ok_dag, ok_der, ok_ops]),
            "integral": ok_int, "sum": ok_sum, "limit": ok_lim,
            "adjoint": ok_dag, "derivative": ok_der, "operators": ok_ops}


if __name__ == "__main__":
    for s in ("I^5_0 f dx", "S^n_{k=1} 1/k**2", "P^n_{k=1} (1 - 1/k)",
              "L_{x->0} sin(x)/x", "D_x (x**3)", "dag(H)"):
        n = parse(s)
        print(f"{s:24s} -> {n.kind:11s} var={n.var} lo={n.lo} hi={n.hi} to={n.to}"
              f"  ops={operators(n)}")
    print(verify())
