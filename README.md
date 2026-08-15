# LookLab WB

**LookLab WB only.** Part of the Luma Color System.

This repository intentionally does **not** include LookLab FullGrade or its creative presets.

## Current source

- Version: **3.0**
- DCTL: `LookLab-WB-v3.0.dctl`
- Input / Output: ARRI Wide Gamut 3 / LogC3 EI800
- License: MIT
- SHA-256: `c8616ec8623318069c73cdb07811a9bd6a4efe7bb57aa5181c6a1102baff5b58`

LookLab WB retains the established WB Source -> Target matrices and Tint fixes. Its neutral state is designed as an exact bypass.

## System role

`Camera/CST -> LookLab WB -> FilmMatrix -> Advanced Toner -> Lens/optical -> Keystone -> ODT`

Recommended Resolve node tree:

1. Camera/CST or input transform
2. **LookLab WB** for source/target white balance and tint
3. FilmMatrix or film-matrix prep
4. [Advanced Toner](https://github.com/wbrisenold/AdvancedToner) for environmental palette and narrative color
5. [PresenceOFX](https://github.com/wbrisenold/PresenceOFX) for lens/optical presence
6. [Keystone](https://github.com/wbrisenold/Keystone) for primary balance, tone, color volume, and cleanup
7. LookLab creative/full-grade stage, when used
8. [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX) as an optional look-LUT browser/audition node before ODT
9. ODT/display transform

- **LookLab WB**: source/target white balance + tint.
- **Advanced Toner**: palette/environment.
- **Keystone**: primary balance and technical grade.

Companion repositories in the same system: [Advanced Toner](https://github.com/wbrisenold/AdvancedToner), [Keystone](https://github.com/wbrisenold/Keystone), [PresenceOFX](https://github.com/wbrisenold/PresenceOFX), and [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX).

## Install

Run `scripts/INSTALL.command`, then refresh Resolve's DCTL/LUT list or restart Resolve.

## Releases

Every push/PR runs static validation. Push a `v*` tag to create a GitHub Release ZIP automatically.
