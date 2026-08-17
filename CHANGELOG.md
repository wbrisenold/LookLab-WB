# Changelog

## 3.1

- Extended Creative White from the legacy D50-D93 set to a 4000 K-25000 K daylight-locus range.
- Preserved the legacy D50, D55, D60, D65, D75, and D93 coefficient values so existing selections do not shift.
- Kept D65 as the exact neutral Creative White state.
- Added numerical white-point regression tests.
- Added exhaustive control-combination transform regression tests.
- Strengthened CI to validate UI mappings, WB matrix completeness, matrix safety, repository version/hash consistency, and installer/source consistency.
- Fixed the macOS installer to install `LookLab-WB-v3.1.dctl`.
- Added a catastrophic-negative encode-domain guard: normal extended negatives are untouched; only values that would encode below LogC3 code -1.0 are compressed toward the neutral axis before re-encoding.
- The tagged release package now includes install/uninstall scripts.
