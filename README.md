# LookLab WB

LookLab WB is a scene-referred white-balance DCTL for ARRI Wide Gamut 3 / LogC3 EI800. It combines source-to-target white-balance matrices, green/magenta tint correction, and a creative white-point selector in one early-pipeline node.

## Source

- Version: `3.1`
- DCTL: `LookLab-WB-v3.1.dctl`
- Input: ARRI Wide Gamut 3 / LogC3 EI800
- Output: ARRI Wide Gamut 3 / LogC3 EI800
- License: MIT
- SHA-256: `a9859cd59796570078bd7233af9e15057b837dbd5f99b44daed3451ef21b2388`

The neutral state is an exact code-value bypass: `WB / Target = Off`, `Tint / Preset = Off`, and `White / Point = D65` returns the input RGB values without a LogC round trip.

## Controls

- `WB / Source`: 2200 K through 10000 K source illuminant selection.
- `WB / Target`: Off, 3200 K, 4300 K, 5500 K, 5600 K, or 6500 K.
- `Tint / Preset`: three green-fix and three magenta-fix strengths.
- `White / Point`: 25000 K Daylight, 20000 K Daylight, 15000 K Daylight, 12000 K Daylight, 10000 K Daylight, D93, D75, D65, D60, D55, D50, 4500 K Daylight, or 4000 K Daylight. D65 is neutral.

The white-point control preserves the former Keystone D93/D75/D65/D60/D55/D50 behavior. The added points extend the same D65-to-target CAT02 construction along the CIE daylight locus. The highlight-weighted blend is preserved from the legacy control, so this is a creative white-point treatment rather than a replacement for the source/target WB correction.

## Placement

Place LookLab WB after the camera/input transform has produced AWG3 / LogC3 EI800 and before FilmMatrix, palette work, lens/optical character, Keystone, and the ODT.

Recommended Resolve node tree:

1. Camera/CST or input transform to AWG3 / LogC3 EI800
2. LookLab WB
3. FilmMatrix or film-matrix prep
4. [Advanced Toner](https://github.com/wbrisenold/AdvancedToner)
5. [PresenceOFX](https://github.com/wbrisenold/PresenceOFX)
6. [Keystone](https://github.com/wbrisenold/Keystone)
7. ODT/display transform
8. [LUTManagerOFX](https://github.com/wbrisenold/LUTManagerOFX), optional after the ODT

FilmMatrix credit: the PD FilmMatrix node in this tree refers to [`PD-LogC3-FilmMatrix.dctl`](https://github.com/mikaelsundell/photographic-dctls/blob/master/PD-LogC3-FilmMatrix.dctl) from Mikael Sundell's `photographic-dctls` repository. It is a separate third-party node and is not included in this repository.

## Technical basis

The DCTL uses ARRI's published EI800 LogC3 exposure-value constants and ALEXA Wide Gamut RGB / XYZ D65 matrix values. Creative-white targets use CAT02 adaptation from D65. The extended daylight targets are generated from CIE daylight chromaticities within the 4000 K to 25000 K range used by the D-illuminant construction.

Primary references:

- ARRI, *ALEXA Log C Curve – Usage in VFX*: https://www.arri.com/resource/blob/31918/66f56e6abb6e5b6553929edf9aa7483e/2017-03-alexa-logc-curve-in-vfx-data.pdf
- CIE 015:2018, *Colorimetry, 4th Edition*: https://www.cie.co.at/publications/colorimetry-4th-edition
- CIE daylight-component data: https://cie.co.at/datatable/components-relative-spectral-distribution-daylight
- CIE 160:2004, *A review of chromatic adaptation transforms*: https://www.cie.co.at/publications/review-chromatic-adaptation-transforms

## Install on macOS

Run:

`scripts/INSTALL.command`

It installs the DCTL under:

`~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Support/LUT/Luma Color System/LookLab WB`

Refresh Resolve's LUT/DCTL list or restart Resolve after installation.

To remove LookLab WB, run `scripts/UNINSTALL.command`.

## Validation

Run all repository checks with:

```bash
python3 ci/validate_dctl.py
python3 ci/test_whitepoint_math.py
python3 ci/test_transform_regression.py
```

CI verifies UI mappings, exact neutral bypass, all 125 WB matrix branches, legacy white-point coefficient preservation, AWG3/XYZ matrix round-trip, LogC3 behavior, white-point chromaticities, matrix invertibility, and every UI-control combination against representative negative/toe/midtone/highlight inputs.

Every push and pull request runs these checks. A `v*` tag packages and publishes a release ZIP.

## Runtime qualification

Static and numerical CI cannot replace a DaVinci Resolve host test. Before using a release on paid or archival work, load the DCTL in the target Resolve version, confirm it compiles on the target GPU backend, verify D65/Off/Off bypass with a difference node, inspect scopes at the 4000 K and 25000 K endpoints, and test representative real footage.

This project was developed with AI assistance. The repository keeps deterministic tests and source references so behavior can be independently checked rather than accepted from generated code alone.
