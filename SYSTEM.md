# Luma Color System

This repository is the **WB-only LookLab tool**.

Recommended current pipeline:

`Camera/CST -> LookLab WB -> FilmMatrix -> Advanced Toner -> PresenceOFX -> Keystone -> ODT -> LUTManagerOFX`

Resolve node tree:

1. Camera/CST or input transform
2. [LookLab WB](https://github.com/wbrisenold/LookLab-WB)
3. FilmMatrix or film-matrix prep
4. [Advanced Toner](https://github.com/wbrisenold/AdvancedToner)
5. [PresenceOFX](https://github.com/wbrisenold/PresenceOFX)
6. [Keystone](https://github.com/wbrisenold/Keystone)
7. ODT/display transform
8. [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX), optional for Rec.709/display LUT auditioning

LookLab WB handles white-balance source/target conversion and tint correction. It does not contain creative presets or a final-look stage.

FilmMatrix credit: the FilmMatrix node refers to [`PD-LogC3-FilmMatrix.dctl`](https://github.com/mikaelsundell/photographic-dctls/blob/master/PD-LogC3-FilmMatrix.dctl) from Mikael Sundell's `photographic-dctls` repository. I did not make that DCTL; I only use it in this node tree.

Repositories: [Advanced Toner](https://github.com/wbrisenold/AdvancedToner), [LookLab WB](https://github.com/wbrisenold/LookLab-WB), [Keystone](https://github.com/wbrisenold/Keystone), [PresenceOFX](https://github.com/wbrisenold/PresenceOFX), [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX).
