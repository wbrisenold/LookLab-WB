# Luma Color System

This repository is the **WB-only LookLab tool**.

Recommended current pipeline:

`Camera/CST -> LookLab WB -> FilmMatrix -> Advanced Toner -> Lens/optical -> Keystone -> ODT`

Resolve node tree:

1. Camera/CST or input transform
2. [LookLab WB](https://github.com/wbrisenold/LookLab-WB)
3. FilmMatrix or film-matrix prep
4. [Advanced Toner](https://github.com/wbrisenold/AdvancedToner)
5. [PresenceOFX](https://github.com/wbrisenold/PresenceOFX)
6. [Keystone](https://github.com/wbrisenold/Keystone)
7. LookLab creative/full-grade stage, when used
8. [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX), optional for look LUT auditioning
9. ODT/display transform

LookLab WB handles white-balance source/target conversion and tint correction. It does not contain the LookLab creative/full-grade engine.

Repositories: [Advanced Toner](https://github.com/wbrisenold/AdvancedToner), [LookLab WB](https://github.com/wbrisenold/LookLab-WB), [Keystone](https://github.com/wbrisenold/Keystone), [PresenceOFX](https://github.com/wbrisenold/PresenceOFX), [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX).
