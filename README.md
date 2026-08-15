# LookLab WB

LookLab WB is a white-balance-only DCTL for source/target white balance and tint correction. It is part of the Luma Color System, but it does not include creative presets or a final-look stage.

## Source

- Version: `3.0`
- DCTL: `LookLab-WB-v3.0.dctl`
- Input: ARRI Wide Gamut 3 / LogC3 EI800
- Output: ARRI Wide Gamut 3 / LogC3 EI800
- License: MIT
- SHA-256: `c8616ec8623318069c73cdb07811a9bd6a4efe7bb57aa5181c6a1102baff5b58`

Its neutral state is designed as an exact bypass.

## Placement

Place LookLab WB near the start of the node tree, after input transform if one is needed and before FilmMatrix, Advanced Toner, PresenceOFX, or Keystone.

Recommended Resolve node tree:

1. Camera/CST or input transform
2. LookLab WB for source/target white balance and tint correction
3. FilmMatrix or film-matrix prep
4. [Advanced Toner](https://github.com/wbrisenold/AdvancedToner) for palette, environment, and mood
5. [PresenceOFX](https://github.com/wbrisenold/PresenceOFX) for lens/optical presence
6. [Keystone](https://github.com/wbrisenold/Keystone) for primary balance, tone, color volume, gamut handling, and cleanup
7. ODT/display transform
8. [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX), optional, for display-referred LUT browsing after the ODT

In this published set, this is the only LookLab repo, and it is only the WB tool.

FilmMatrix credit: the PD FilmMatrix node in this tree refers to [`PD-LogC3-FilmMatrix.dctl`](https://github.com/mikaelsundell/photographic-dctls/blob/master/PD-LogC3-FilmMatrix.dctl) from Mikael Sundell's `photographic-dctls` repository. I did not make that DCTL. I only use it as a separate node in my Resolve node tree.

## Related Repositories

- [Advanced Toner](https://github.com/wbrisenold/AdvancedToner): scene-referred palette and environment toning
- [PD-LogC3-FilmMatrix.dctl](https://github.com/mikaelsundell/photographic-dctls/blob/master/PD-LogC3-FilmMatrix.dctl): third-party FilmMatrix node used in the tree; not made by me
- [Keystone](https://github.com/wbrisenold/Keystone): technical balancing and cleanup hub
- [PresenceOFX](https://github.com/wbrisenold/PresenceOFX): lens/optical presence OFX
- [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX): folder-backed LUT browsing OFX, usually after ODT for Rec.709/display LUTs

## Install on macOS

Run `scripts/INSTALL.command`. It installs the DCTL into Resolve's user LUT/DCTL folder under:

`Luma Color System/LookLab WB`

Refresh Resolve's LUT list or restart Resolve after installing.

## Validation and Releases

Run static validation with:

```bash
python3 ci/validate_dctl.py
```

Every push and pull request runs the validator. A `v*` tag creates a release ZIP automatically.

## Disclaimer

This tool was vibe coded with AI assistance. Treat it as an experimental grading tool, not a color-science reference implementation. Validate it on your footage, scopes, and delivery path before using it on paid or archival work.

This repository intentionally excludes creative presets and final-look behavior.
