#!/usr/bin/env python3
"""Numerical regression checks for LookLab Creative White CAT02 matrices."""
from pathlib import Path
import math, re, sys

p = next((Path(__file__).resolve().parents[1] / 'dctl').glob('*.dctl'))
t = p.read_text(encoding='utf-8')

# D65 source white used by OpenDRT.
sx, sy = 0.3127, 0.3290
src = (sx/sy, 1.0, (1.0-sx-sy)/sy)

def dxy(T):
    if 4000 <= T <= 7000:
        x = 0.244063 + 0.09911e3/T + 2.9678e6/(T*T) - 4.6070e9/(T*T*T)
    elif 7000 < T <= 25000:
        x = 0.237040 + 0.24748e3/T + 1.9018e6/(T*T) - 2.0064e9/(T*T*T)
    else:
        raise ValueError(T)
    y = -3.0*x*x + 2.87*x - 0.275
    return (x,y)

expected = {
    0:dxy(25000), 1:dxy(20000), 2:dxy(15000), 3:dxy(12000), 4:dxy(10000),
    5:(0.283,0.297), 6:(0.29903,0.31488), 7:(0.3127,0.3290),
    8:(0.32162624,0.337737), 9:(0.33243,0.34744), 10:(0.3457,0.3585),
    11:dxy(4500), 12:dxy(4000),
}

fn = t[t.index('__DEVICE__ float3 ll_creative_white_cat'):t.index('__DEVICE__ float ll_scene_tsn')]

def matrix_for(idx):
    if idx == 7:
        return [[1,0,0],[0,1,0],[0,0,1]]
    m = re.search(rf'if\(wp=={idx}\).*?return ll_rowmul\(xyz,\s*(.*?)\);', fn, re.S)
    if not m:
        raise RuntimeError(f'missing matrix for wp {idx}')
    nums = [float(x[:-1]) for x in re.findall(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?[fF]', m.group(1))]
    if len(nums) != 9:
        raise RuntimeError(f'wp {idx}: expected 9 coefficients, found {len(nums)}')
    return [nums[0:3], nums[3:6], nums[6:9]]

def mv(M,v): return tuple(sum(M[r][k]*v[k] for k in range(3)) for r in range(3))
def det(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

ok = True
for idx in range(13):
    M = matrix_for(idx)
    d = det(M)
    if not math.isfinite(d) or d <= 0.5:
        print(f'[FAIL] wp {idx}: determinant {d}')
        ok = False
        continue
    out = mv(M,src)
    out = tuple(v/out[1] for v in out)
    s = sum(out)
    xy = (out[0]/s, 1.0/s)
    err = max(abs(xy[0]-expected[idx][0]), abs(xy[1]-expected[idx][1]))
    tol = 1e-6
    if err > tol:
        print(f'[FAIL] wp {idx}: xy={xy}, expected={expected[idx]}, err={err}')
        ok = False
    else:
        print(f'[PASS] wp {idx}: xy={xy[0]:.9f},{xy[1]:.9f} det={d:.6f}')
if not ok:
    sys.exit(1)
