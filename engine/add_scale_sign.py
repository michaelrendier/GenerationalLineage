"""
SedenionFactoralRelativity.engine.add_scale_sign
================================================
THE ADD:SCALE:SIGN DATATYPE, as an ENGINE in the decomposer suite.

The tier-0 floor  Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN),  x ↦ sign·scale·x + add,
as a composable / invertible / decomposable value type. This is the piece
every roll-down in `lineage.py` (`root_irreducible`, `ROOT_OF`, `AFF1`)
terminates on — here it is an object you can hold, not just a label.

Standalone port per this repo's module-independence convention (cf.
`lineage.py` `ring_chart_gamma` / ValaQuenta's own copy) — NOT a cross-repo
import of `ValaQuenta.modules.add_scale_sign`. Same maths, verified the same
way (round-trip 1e-12, fold = tanh, firing defect = (g−1)·ln s exactly).

Generalized equation:  u = Σ_k [ g_k·ln s_k + a_k ] ,  Γ = tanh(u/2).
Ground state a=0,s=1,g=+1 ⇒ u=0 ⇒ Γ=0 (the now).

The FAST INVERSE SQUARE ROOT (Quake III, 0x5f3759df) is the canonical worked
example: 1/√x = exp(−½·ln x) is an ADD:SCALE:SIGN word computed in the IEEE
exponent field (the hardware's native log₂), SKIPPING the SCALE-multiply —
SIGN(−) + SCALE(½ via >>1) + ADD(the magic constant) → "good enough", then
one Newton step. See `fast_inverse_sqrt` / `fisr_word`.
"""
from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

IDENTITIES = (0.0, 1.0, 1)
BRACKET = "[SCALE, ADD] = ADD"
CAMSHAFT = ("SIGN", "SCALE", "ADD")          # SIGN fires first / innermost


def _gamma(u: float) -> float:
    return math.tanh(0.5 * u)


@dataclass(frozen=True)
class ASS:
    """x ↦ sign·scale·x + add. Compose @, invert ~, apply by call."""
    add: float = 0.0
    scale: float = 1.0
    sign: int = 1
    steps: Tuple["ASS", ...] = field(default=(), compare=False, repr=False)

    def __post_init__(self):
        if self.scale <= 0:
            raise ValueError("SCALE must be > 0; a negative gain is SCALE∘SIGN")
        if self.sign not in (-1, 1):
            raise ValueError("SIGN must be ±1")
        if not self.steps:
            object.__setattr__(self, "steps", (self,))

    @classmethod
    def ADD(cls, a: float) -> "ASS":   return cls(float(a), 1.0, 1)
    @classmethod
    def SCALE(cls, s: float) -> "ASS": return cls(0.0, float(s), 1)
    @classmethod
    def SIGN(cls, g: int) -> "ASS":    return cls(0.0, 1.0, int(g))

    def __call__(self, x: float) -> float:
        return self.sign * self.scale * x + self.add

    def __matmul__(self, other: "ASS") -> "ASS":
        if not isinstance(other, ASS):
            return NotImplemented
        return ASS(self.add + self.sign * self.scale * other.add,
                   self.scale * other.scale, self.sign * other.sign,
                   steps=other.steps + self.steps)

    def then(self, other: "ASS") -> "ASS":
        return other @ self

    def _is_atomic(self) -> bool:
        return len(self.steps) == 1 and self.steps[0] is self

    def __invert__(self) -> "ASS":
        a = -self.sign * self.add / self.scale + 0.0
        s, g = 1.0 / self.scale, self.sign
        if self._is_atomic():
            return ASS(a, s, g)
        inv = ASS(a, s, g)
        object.__setattr__(inv, "steps", tuple(~st for st in reversed(self.steps)))
        return inv

    backward = __invert__

    def residual(self, without: str) -> "ASS":
        w = without.upper()
        if w == "ADD":   return ASS(0.0, self.scale, self.sign)
        if w == "SCALE": return ASS(self.add, 1.0, self.sign)
        if w == "SIGN":  return ASS(self.add, self.scale, 1)
        raise ValueError("without must be ADD, SCALE or SIGN")

    def only(self, part: str) -> "ASS":
        p = part.upper()
        if p == "ADD":   return ASS.ADD(self.add)
        if p == "SCALE": return ASS.SCALE(self.scale)
        if p == "SIGN":  return ASS.SIGN(self.sign)
        raise ValueError("part must be ADD, SCALE or SIGN")

    def parts(self) -> Tuple["ASS", "ASS", "ASS"]:
        return (ASS.SIGN(self.sign), ASS.SCALE(self.scale), ASS.ADD(self.add))

    def is_ground(self, tol: float = 1e-12) -> bool:
        return abs(self.add) <= tol and abs(self.scale - 1.0) <= tol and self.sign == 1

    def u(self) -> float:
        return self.sign * math.log(self.scale) + self.add

    def gamma(self) -> float:
        return _gamma(self.u())

    def is_additive(self) -> bool:
        return self.sign == 1 or abs(self.scale - 1.0) < 1e-12

    def firing_defect(self) -> float:
        """u − (a + ln s) = (g − 1)·ln s.  Non-zero ⇔ SIGN flipped a
        non-trivial SCALE ⇔ 'defined twice' (cf. the Bell composed-rotation
        defect)."""
        return self.u() - (self.add + math.log(self.scale))

    def to_smith(self) -> Dict[str, Any]:
        gs, ga = _gamma(math.log(self.scale)), _gamma(self.add)
        return {"Γ_SCALE": gs, "Γ_ADD": ga, "parity": self.sign,
                "Γ": self.gamma(), "u": self.u(),
                "at_now": abs(gs) < 1e-12 and abs(ga) < 1e-12 and self.sign == 1,
                "notation": f"Γ_SCALE=tanh(½·ln {self.scale:g})={gs:.6g}  "
                            f"Γ_ADD=tanh(½·{self.add:g})={ga:.6g}  parity {self.sign:+d}"}

    def lineage(self, order: str = "chrono") -> "ASSWord":
        steps = list(self.steps)
        if order == "zeta":
            steps.sort(key=lambda s: abs(s.u()), reverse=True)
        elif order != "chrono":
            raise ValueError("order must be 'chrono' or 'zeta'")
        return ASSWord(tuple(steps), order, self)

    def record(self) -> Tuple[Tuple[float, float, int], ...]:
        return tuple((s.add, s.scale, s.sign) for s in self.steps)

    def camshaft(self) -> Tuple[str, ...]:
        return CAMSHAFT

    def __str__(self) -> str:
        return f"x ↦ {self.sign:+d}·{self.scale:g}·x + {self.add:g}"


ASS.IDENTITY = ASS(*IDENTITIES)
ASS.GROUND = ASS.IDENTITY


@dataclass(frozen=True)
class ASSWord:
    steps: Tuple[ASS, ...]
    order: str
    source: ASS

    def u_total(self) -> float:        return self.source.u()
    def u_generators(self) -> float:   return self.source.add + math.log(self.source.scale)
    def firing_defect(self) -> float:  return self.u_total() - self.u_generators()
    def additive(self) -> bool:        return abs(self.firing_defect()) < 1e-9
    def gamma(self) -> float:          return self.source.gamma()

    def as_equation(self) -> str:
        s = self.source                    # the resulting element — g·ln s + a
        terms = []
        if abs(s.scale - 1.0) > 1e-12:
            terms.append(f"{s.sign:+d}·ln {s.scale:g}")
        if abs(s.add) > 1e-12 or not terms:
            terms.append(f"{s.add:+g}")
        body = " + ".join(terms)
        tail = "" if self.additive() else \
            f"    [firing defect {self.firing_defect():+.3g}: SIGN flipped a non-trivial SCALE]"
        return f"u = {body} = {self.u_total():.6g}    Γ = tanh(u/2) = {self.gamma():.6g}{tail}"

    def __iter__(self):  return iter(self.steps)
    def __len__(self):   return len(self.steps)
    def __str__(self) -> str:
        return f"ASSWord[{self.order}]  ({len(self.steps)} steps)\n  {self.as_equation()}"


def compose(*elements: ASS) -> ASS:
    if not elements:
        return ASS.IDENTITY
    out = elements[0]
    for e in elements[1:]:
        out = e @ out
    return out


def word(u: float) -> ASS:
    """The pure-SCALE element with word u  (Γ = tanh(u/2))."""
    return ASS.SCALE(math.exp(u))


# ════════════════════════════════════════════════════════════════════════
#  THE FAST INVERSE SQUARE ROOT  —  ADD:SCALE:SIGN in the hardware's log₂
# ════════════════════════════════════════════════════════════════════════
_MAGIC32 = 0x5f3759df


def fast_inverse_sqrt(x: float, newton: int = 1) -> float:
    """Quake III Q_rsqrt, faithfully: bit-cast float32 → int32, one ADD in
    the integer (log₂) domain,  i = MAGIC − (i >> 1),  cast back, then
    `newton` Newton steps of  y ← y·(1.5 − 0.5·x·y²)."""
    i = struct.unpack("<i", struct.pack("<f", x))[0]
    i = _MAGIC32 - (i >> 1)
    y = struct.unpack("<f", struct.pack("<i", i))[0]
    for _ in range(newton):
        y = y * (1.5 - 0.5 * x * y * y)
    return y


def fisr_word(x: float) -> Dict[str, Any]:
    """1/√x = exp(−½·ln x) read as an ADD:SCALE:SIGN word:

        SIGN(−1) ∘ SCALE(½) ∘ ADD(bias-offset)      on  log₂(x)

    The FISR computes exactly this in the IEEE-754 exponent field —
    `>> 1` is SCALE by ½ done as a shift (SCALE *skipped* as a float
    multiply), `MAGIC − …` is the ADD, the sign bit is untouched (SIGN).
    The float mantissa makes it piecewise-linear = "good enough"; the
    Newton step is the residual.
    """
    approx = fast_inverse_sqrt(x, newton=0)
    exact = 1.0 / math.sqrt(x)
    one_step = fast_inverse_sqrt(x, newton=1)
    # the same result as an ASS word on ln x:  u = −½·ln x  (SIGN·SCALE), ADD=0
    W = compose(ASS.SCALE(0.5), ASS.SIGN(-1))          # x ↦ −½·x  on ln-values
    u = W(math.log(x))
    return {
        "x": x,
        "ASS_word_on_ln_x": str(W),
        "u = −½·ln x": u,
        "exp(u) = 1/√x (exact)": math.exp(u),
        "1/√x exact": exact,
        "FISR raw (no Newton)": approx,
        "raw rel error": abs(approx - exact) / exact,
        "FISR + 1 Newton": one_step,
        "1-step rel error": abs(one_step - exact) / exact,
        "reading": "SIGN(−) + SCALE(½ as >>1) + ADD(magic); SCALE-multiply skipped; "
                   "mantissa linearity = 'good enough'; Newton = the residual",
    }


def reduces_everything(op: str) -> Dict[str, Any]:
    """Tie-in to the roll-down: any named operation → its tier-0 root, then
    the root as a live ASS generator. 'this reduces everything' — literally."""
    from .lineage import root_irreducible
    r = root_irreducible(op)
    root = r.get("root") if isinstance(r, dict) else r
    gen = {"ADD": ASS.ADD(1.0), "SCALE": ASS.SCALE(2.0), "SIGN": ASS.SIGN(-1)}.get(root)
    return {"operation": op, "root": root, "as_generator": str(gen) if gen else None,
            "detail": r}
