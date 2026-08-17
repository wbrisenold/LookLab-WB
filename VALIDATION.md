# Validation

Release source: `dctl/LookLab-WB-v3.1.dctl`

SHA-256: `a9859cd59796570078bd7233af9e15057b837dbd5f99b44daed3451ef21b2388`

## Automated release gates

- DCTL structure and balanced delimiters
- Resolve `transform` entry point and UI declarations
- unique UI IDs and combo enum/label parity
- no UI/combo identifier collisions with `__DEVICE__` function names
- exact D65 neutral bypass contract
- all 125 WB source/target branches present
- matching WB source/target identity branches
- legacy D50-D93 Creative White coefficients preserved
- AWG3/XYZ matrices numerically inverse
- LogC3 constants and negative/toe/highlight round-trip checks
- all Creative White matrices finite, invertible, and mapped to expected target chromaticities
- every UI-control combination evaluated on representative LogC inputs with finite outputs
- README version, filename, and SHA-256 consistency
- installer source-path consistency

Run:

```bash
python3 ci/validate_dctl.py
python3 ci/test_whitepoint_math.py
python3 ci/test_transform_regression.py
```

## Host qualification still required

The automated suite does not compile DCTL inside DaVinci Resolve. A release should still be smoke-tested in the target Resolve version and GPU backend before production deployment.
