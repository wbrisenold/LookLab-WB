#!/usr/bin/env python3
from pathlib import Path
import hashlib, math, re, sys

root = Path(__file__).resolve().parents[1]
files = list((root / 'dctl').glob('*.dctl'))
if len(files) != 1:
    print(f'[FAIL] expected exactly one DCTL, found {len(files)}')
    sys.exit(1)
p = files[0]
t = p.read_text(encoding='utf-8')

checks = {}
def check(name, value):
    checks[name] = bool(value)

check('non-empty source', len(t) > 500)
check('transform entry point', '__DEVICE__ float3 transform(' in t)
check('UI parameters present', 'DEFINE_UI_PARAMS(' in t)
check('balanced parentheses', t.count('(') == t.count(')'))
check('balanced braces', t.count('{') == t.count('}'))
check('balanced brackets', t.count('[') == t.count(']'))
check('no merge-conflict markers', re.search(r'^(<<<<<<<|=======|>>>>>>>)', t, re.M) is None)
check('SPDX present', 'SPDX-License-Identifier:' in t)

# UI identifiers must be unique and must not collide with device function names.
ui_ids = re.findall(r'DEFINE_UI_PARAMS\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,', t)
check('unique UI parameter identifiers', len(ui_ids) == len(set(ui_ids)))
enum_ids = set()
combo_matches = list(re.finditer(
    r'DEFINE_UI_PARAMS\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,.*?DCTLUI_COMBO_BOX\s*,\s*([0-9]+)\s*,\s*\{([^{}]+)\}\s*,\s*\{([^{}]+)\}\s*\)',
    t, re.S))
combo_counts_ok = True
combo_defaults_ok = True
for m in combo_matches:
    default = int(m.group(2))
    enums = [x.strip() for x in m.group(3).split(',')]
    labels = [x.strip() for x in m.group(4).split(',')]
    combo_counts_ok &= len(enums) == len(labels) and len(enums) > 0
    combo_defaults_ok &= 0 <= default < len(enums)
    enum_ids.update(x for x in enums if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', x))
check('combo enum/label counts match', combo_counts_ok)
check('combo defaults in range', combo_defaults_ok)
fn_ids = set(re.findall(r'__DEVICE__\s+(?:float|float2|float3|int|bool)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', t))
check('no Metal UI/function symbol collisions', not ((set(ui_ids) | enum_ids) & fn_ids))

# v3.1 Creative White contract.
wp = re.search(
    r'DEFINE_UI_PARAMS\(creative_whitepoint,\s*White / Point,\s*DCTLUI_COMBO_BOX,\s*(\d+),\s*\{([^}]+)\},\s*\{([^}]+)\}\)', t)
expected_wp_enums = ['wp_d250','wp_d200','wp_d150','wp_d120','wp_d100','wp_d93','wp_d75','wp_d65','wp_d60','wp_d55','wp_d50','wp_d45','wp_d40']
expected_wp_labels = ['25000K Daylight','20000K Daylight','15000K Daylight','12000K Daylight','10000K Daylight','D93','D75','D65','D60','D55','D50','4500K Daylight','4000K Daylight']
wp_ok = False
if wp:
    wp_default = int(wp.group(1))
    wp_enums = [x.strip() for x in wp.group(2).split(',')]
    wp_labels = [x.strip() for x in wp.group(3).split(',')]
    wp_ok = wp_default == 7 and wp_enums == expected_wp_enums and wp_labels == expected_wp_labels
check('Creative White range/order/default', wp_ok)
check('Creative White clamp range', 'int wp=clampi((int)(creative_whitepoint+0.5f),0,12);' in t)
check('D65 exact neutral bypass', 'if(tgt==0 && tint==0 && wp==7)' in t and 'if(wp==7)return awg3;' in t)

# Existing grades: the original OpenDRT-derived coefficient rows must remain literal.
legacy_rows = [
    '0.95703423023223877f,-0.0247171502560377121f,0.0624028593301773071f',
    '0.981001079082489014f,-0.0116619253531098366f,0.0265614092350006104f',
    '1.01182246208190918f,0.00778879318386316299f,-0.0157783031463623047f',
    '1.02585089206695557f,0.0179439820349216461f,-0.0332137793302536011f',
    '1.04257404804229736f,0.03089117631316185f,-0.052812620997428894f',
]
check('legacy D50-D93 coefficients preserved', all(row in t for row in legacy_rows))

# WB matrix table must be complete and exact identity where source==target.
wb_start = t.find('__DEVICE__ float3 apply_wb_preset')
wb_end = t.find('// ---------------- Creative White', wb_start)
wb = t[wb_start:wb_end] if wb_start >= 0 and wb_end > wb_start else ''
complete = True
for target in range(1, 6):
    start = wb.find(f'if(target_id=={target})')
    end = wb.find(f'if(target_id=={target+1})', start) if target < 5 else wb.rfind('  return rgb;')
    block = wb[start:end] if start >= 0 and end > start else ''
    ids = {int(x) for x in re.findall(r'if\(source_id==(\d+)\)', block)}
    complete &= ids == set(range(25))
check('all 125 WB source/target branches present', complete)
identity_pairs = {1:5, 2:10, 3:15, 4:16, 5:18}
identity_ok = all(re.search(rf'if\(target_id=={tid}\).*?if\(source_id=={sid}\)return rgb;', wb, re.S) for tid, sid in identity_pairs.items())
check('matching WB source/target pairs are identity', identity_ok)

# Matrix arithmetic sanity: verify AWG3 <-> XYZ constants are inverses to tight tolerance.
def floats_from_macro(name):
    m = re.search(rf'#define {name} make_float3\(([^)]+)\)', t)
    return [float(x.strip().rstrip('f')) for x in m.group(1).split(',')] if m else None
cols_a = [floats_from_macro(f'LL_AWG3_XYZ_C{i}') for i in range(3)]
cols_b = [floats_from_macro(f'LL_XYZ_AWG3_C{i}') for i in range(3)]
def mat_from_cols(cols): return [[cols[c][r] for c in range(3)] for r in range(3)]
def mm(a,b): return [[sum(a[r][k]*b[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
if all(cols_a) and all(cols_b):
    prod = mm(mat_from_cols(cols_b), mat_from_cols(cols_a))
    inv_err = max(abs(prod[r][c] - (1.0 if r == c else 0.0)) for r in range(3) for c in range(3))
else:
    inv_err = 1.0
check('AWG3/XYZ matrices are inverse', inv_err < 1e-9)

# LogC3 code-path invariants.
check('LogC3 constants present', all(x in t for x in ['LOGC3_CUT','LOGC3_A','LOGC3_B','LOGC3_C','LOGC3_D','LOGC3_E','LOGC3_F','LOGC3_CODE_CUT']))
check('no output clamp added', 'clampf3(' not in t and 'saturate' not in t.lower())
check('encode-domain safety floor present', '#define LL_SAFE_LINEAR_MIN -0.203591513f' in t and 'll_encode_domain_guard(lin)' in t)

# Repository packaging integrity: source filename/version/hash and installer must agree.
actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
readme = (root / 'README.md').read_text(encoding='utf-8')
installer = (root / 'scripts' / 'INSTALL.command').read_text(encoding='utf-8')
check('release filename is v3.1', p.name == 'LookLab-WB-v3.1.dctl')
check('README version is v3.1', '- Version: `3.1`' in readme)
check('README source filename matches', f'- DCTL: `{p.name}`' in readme)
check('README source hash matches', actual_hash in readme)
check('README documents full white-point endpoints', ('25000K' in readme or '25000 K' in readme) and ('4000K' in readme or '4000 K' in readme))
check('installer references release source', f'SRC="$ROOT/dctl/{p.name}"' in installer)
uninstaller_path = root / 'scripts' / 'UNINSTALL.command'
check('uninstaller present', uninstaller_path.is_file())
workflow = (root / '.github' / 'workflows' / 'validate-release.yml').read_text(encoding='utf-8')
check('workflow runs white-point math test', 'python3 ci/test_whitepoint_math.py' in workflow)
check('workflow runs transform regression test', 'python3 ci/test_transform_regression.py' in workflow)
check('release packages validation docs', 'VALIDATION.md' in workflow and 'CHANGELOG.md' in workflow)
check('release packages install scripts', 'cp -R dctl scripts README.md' in workflow)

for name, ok in checks.items():
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if not all(checks.values()):
    sys.exit(1)
print('SHA-256:', actual_hash)
