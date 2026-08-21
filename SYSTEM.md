# Luma Color System

This repository is the **LookLab WB** tool.

Recommended current pipeline:

`Camera/CST -> PresenceOFX -> Keystone -> PrimeraSkin -> HB Color Separation -> KH Gamut Compressor -> Referent ODT -> FilmBox -> MonoNodes`

LookLab WB owns early white-balance work: source/target WB, tint correction, and creative white-point selection. Its creative White Point range extends from 4000 K Daylight through 25000 K Daylight, with D65 as the neutral state.

Keystone remains the main technical grading hub and now owns the normal Bradford Kelvin/Tint correction. LookLab WB is an optional pre-PresenceOFX stage for shots that intentionally need its separate white-point behavior.

FilmMatrix is a separate third-party node. The pipeline reference uses [`PD-LogC3-FilmMatrix.dctl`](https://github.com/mikaelsundell/photographic-dctls/blob/master/PD-LogC3-FilmMatrix.dctl) from Mikael Sundell's `photographic-dctls` repository; it is not included here.

Repositories: [LookLab WB](https://github.com/wbrisenold/LookLab-WB), [Keystone](https://github.com/wbrisenold/Keystone), [PresenceOFX](https://github.com/wbrisenold/PresenceOFX), [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX).
