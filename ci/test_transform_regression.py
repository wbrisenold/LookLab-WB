#!/usr/bin/env python3
"""Behavioral regression tests for LookLab WB v3.1.

Pure-Python mirror of the DCTL's matrix/LogC path. It parses coefficients from
source so CI catches missing branches, malformed matrices, NaN/Inf behavior,
and control mapping regressions without requiring DaVinci Resolve on the runner.
"""
from pathlib import Path
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DCTL = next((ROOT / "dctl").glob("*.dctl"))
T = DCTL.read_text(encoding="utf-8")


def fail(msg):
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def pass_(msg):
    print(f"[PASS] {msg}")


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def mv(m, v):
    return tuple(sum(m[r][k] * v[k] for k in range(3)) for r in range(3))


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def macro(name):
    m = re.search(rf"#define\s+{name}\s+([^\s]+)", T)
    if not m:
        fail(f"missing macro {name}")
    return float(m.group(1).rstrip("f"))


CUT = macro("LOGC3_CUT")
A = macro("LOGC3_A")
B = macro("LOGC3_B")
C = macro("LOGC3_C")
D = macro("LOGC3_D")
E = macro("LOGC3_E")
F = macro("LOGC3_F")
CODE_CUT = macro("LOGC3_CODE_CUT")
SAFE_MIN = macro("LL_SAFE_LINEAR_MIN")


def dec1(v):
    return (10.0 ** ((v - D) / C) - B) / A if v > CODE_CUT else (v - F) / E


def enc1(x):
    if x > CUT:
        return C * math.log10(max(A * x + B, 1.0e-30)) + D
    return E * x + F


def dec(v):
    return tuple(dec1(x) for x in v)


def enc(v):
    return tuple(enc1(x) for x in v)


def parse_make_float3(txt):
    nums = [float(x.rstrip("fF")) for x in re.findall(
        r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?[fF]", txt
    )]
    if len(nums) != 9:
        fail(f"expected 9 matrix coefficients, found {len(nums)}")
    # DCTL mmul takes columns.
    c0, c1, c2 = nums[0:3], nums[3:6], nums[6:9]
    return [[c0[r], c1[r], c2[r]] for r in range(3)]


def parse_rowmul(txt):
    nums = [float(x.rstrip("fF")) for x in re.findall(
        r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?[fF]", txt
    )]
    if len(nums) != 9:
        fail(f"expected 9 row-matrix coefficients, found {len(nums)}")
    return [nums[0:3], nums[3:6], nums[6:9]]


def parse_macro_matrix(prefix):
    cols = []
    for i in range(3):
        m = re.search(rf"#define\s+{prefix}_C{i}\s+make_float3\(([^)]+)\)", T)
        if not m:
            fail(f"missing {prefix}_C{i}")
        vals = [float(x.strip().rstrip("f")) for x in m.group(1).split(",")]
        cols.append(vals)
    return [[cols[c][r] for c in range(3)] for r in range(3)]


AWG_TO_XYZ = parse_macro_matrix("LL_AWG3_XYZ")
XYZ_TO_AWG = parse_macro_matrix("LL_XYZ_AWG3")

# Parse 125 WB branches.
wb_start = T.index("__DEVICE__ float3 apply_wb_preset")
wb_end = T.index("// ---------------- Creative White", wb_start)
wb_txt = T[wb_start:wb_end]
WB = {}
for target in range(1, 6):
    start = wb_txt.index(f"if(target_id=={target})")
    end = wb_txt.index(f"if(target_id=={target+1})", start) if target < 5 else wb_txt.rfind("  return rgb;")
    block = wb_txt[start:end]
    for source in range(25):
        identity = re.search(rf"if\(source_id=={source}\)return rgb;", block)
        if identity:
            WB[(source, target)] = [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]
            continue
        m = re.search(
            rf"if\(source_id=={source}\)return mmul\((make_float3\([^;]+?)\),rgb\);",
            block,
        )
        if not m:
            fail(f"missing WB matrix source={source} target={target}")
        WB[(source, target)] = parse_make_float3(m.group(1))
if len(WB) != 125:
    fail(f"expected 125 WB matrices, found {len(WB)}")
pass_("parsed all 125 WB matrices")

# Parse tint matrices.
tint_start = T.index("__DEVICE__ float3 apply_tint_preset")
tint_txt = T[tint_start:T.index("// ---------------- Main", tint_start)]
TINT = {0: [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]}
for idx in range(1, 7):
    m = re.search(rf"if\(tint_id=={idx}\)return mmul\((make_float3\([^;]+?)\),rgb\);", tint_txt)
    if not m:
        fail(f"missing tint matrix {idx}")
    TINT[idx] = parse_make_float3(m.group(1))
pass_("parsed all tint matrices")

# Parse Creative White row matrices.
wp_start = T.index("__DEVICE__ float3 ll_creative_white_cat")
wp_end = T.index("__DEVICE__ float ll_scene_tsn", wp_start)
wp_txt = T[wp_start:wp_end]
WP = {7: [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]}
for idx in list(range(0, 7)) + list(range(8, 13)):
    m = re.search(rf"if\(wp=={idx}\).*?return ll_rowmul\(xyz,\s*(.*?)\);", wp_txt, re.S)
    if not m:
        fail(f"missing white-point matrix {idx}")
    WP[idx] = parse_rowmul(m.group(1))
pass_("parsed all 13 white-point states")

# All adaptation matrices should be finite, invertible, and orientation-preserving.
for group_name, matrices in (("WB", WB.values()), ("Tint", TINT.values()), ("White", WP.values())):
    for m in matrices:
        d = det3(m)
        if not math.isfinite(d) or d <= 0.05:
            fail(f"{group_name} contains invalid/singular matrix det={d}")
pass_("all grading matrices are finite and non-singular")

# LogC3 encode/decode must round-trip across negative, toe, midtone and highlight code values.
for x in (-0.25, -0.05, 0.0, F, CODE_CUT, 0.18, 0.391, 0.5, 0.8, 1.0, 1.2, 1.5):
    rt = enc1(dec1(x))
    if not math.isfinite(rt) or abs(rt - x) > 2.0e-6:
        fail(f"LogC3 round-trip x={x} -> {rt}")
pass_("LogC3 negative/toe/highlight round-trip")


def apply_white(lin, wp):
    if wp == 7:
        return lin
    xyz = mv(AWG_TO_XYZ, lin)
    if xyz[1] <= 1.0e-10:
        return lin
    adapted = mv(WP[wp], xyz)
    tsn = max(0.0, min(1.0, xyz[1] / (xyz[1] + 1.62)))
    blend = math.sqrt(tsn)
    return mv(XYZ_TO_AWG, lerp(xyz, adapted, blend))


def encode_guard(rgb):
    mn = min(rgb)
    if mn >= SAFE_MIN:
        return rgb
    Y = mv(AWG_TO_XYZ, rgb)[1]
    if Y > SAFE_MIN + 1.0e-7:
        d = tuple(rgb[i] - Y for i in range(3))
        s = 1.0
        for x, dd in zip(rgb, d):
            if x < SAFE_MIN and dd < 0.0:
                s = min(s, (SAFE_MIN - Y) / dd)
        s = max(0.0, min(1.0, s))
        return tuple(Y + d[i] * s for i in range(3))
    return tuple(max(x, SAFE_MIN) for x in rgb)


def transform(rgb, source, target, tint, wp):
    # Mirror the DCTL's exact neutral bypass.
    if target == 0 and tint == 0 and wp == 7:
        return rgb
    lin = dec(rgb)
    if target != 0:
        lin = mv(WB[(source, target)], lin)
    if tint != 0:
        lin = mv(TINT[tint], lin)
    if wp != 7:
        lin = apply_white(lin, wp)
    lin = encode_guard(lin)
    return enc(lin)

# Exact neutral bypass for every source selection.
neutral_samples = [
    (-0.1, 0.0, 0.2),
    (0.0, 0.0, 0.0),
    (0.391, 0.391, 0.391),
    (0.18, 0.55, 0.95),
    (1.2, 0.7, -0.05),
]
for source in range(25):
    for rgb in neutral_samples:
        out = transform(rgb, source, 0, 0, 7)
        if out != rgb:
            fail(f"neutral bypass changed source={source}, rgb={rgb}, out={out}")
pass_("exact neutral bypass across all 25 WB source selections")

# Guard must be invisible to ordinary extended negatives and preserve Y when active.
ordinary = (-0.05, 0.2, 0.4)
if encode_guard(ordinary) != ordinary:
    fail("encode guard touched ordinary extended-negative RGB")
pathological = (2.0, -5.0, 0.5)
Y0 = mv(AWG_TO_XYZ, pathological)[1]
guarded = encode_guard(pathological)
Y1 = mv(AWG_TO_XYZ, guarded)[1]
if Y0 > SAFE_MIN + 1.0e-7 and abs(Y1 - Y0) > 1.0e-9:
    fail(f"encode guard changed scene Y: {Y0} -> {Y1}")
if min(guarded) < SAFE_MIN - 1.0e-9:
    fail("encode guard did not enforce linear floor")
pass_("encode-domain guard preserves ordinary negatives and scene Y")

# Exhaust every UI combination on a representative set of legal and extended LogC values.
samples = [
    (-0.10, 0.05, 0.20),
    (0.0, 0.0, 0.0),
    (0.149658, 0.149658, 0.149658),
    (0.391, 0.391, 0.391),
    (0.65, 0.40, 0.20),
    (0.20, 0.55, 0.90),
    (0.90, 0.20, 0.45),
    (1.20, 0.70, 0.10),
]
count = 0
max_abs = 0.0
for source in range(25):
    for target in range(6):
        for tint in range(7):
            for wp in range(13):
                for rgb in samples:
                    out = transform(rgb, source, target, tint, wp)
                    count += 1
                    if not all(math.isfinite(x) for x in out):
                        fail(f"non-finite output controls={(source,target,tint,wp)} rgb={rgb} out={out}")
                    max_abs = max(max_abs, *(abs(x) for x in out))
                    if min(out) < -1.00001:
                        fail(f"encode guard failed: output below -1.0 controls={(source,target,tint,wp)} rgb={rgb} out={out}")
                    if max(out) > 2.0:
                        fail(f"runaway positive output controls={(source,target,tint,wp)} rgb={rgb} out={out}")
pass_(f"{count:,} transform evaluations finite and encode-safe; max |code value|={max_abs:.6f}")

# Added endpoints must have a real effect on a lit neutral patch and D65 must not.
gray = dec((0.5, 0.5, 0.5))
for wp in (0, 12):
    shifted = apply_white(gray, wp)
    if max(abs(shifted[i] - gray[i]) for i in range(3)) < 1.0e-5:
        fail(f"extended white point {wp} is effectively inert")
if apply_white(gray, 7) != gray:
    fail("D65 creative-white state is not exact identity")
pass_("4000 K / 25000 K endpoints active; D65 identity")

print("All LookLab WB behavioral regression checks passed.")
