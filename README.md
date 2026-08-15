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

- **LookLab WB**: source/target white balance + tint.
- **Advanced Toner**: palette/environment.
- **Keystone**: primary balance and technical grade.

Companion OFX tools in the same system: **PresenceOFX** provides the lens/optical presence stage, and **LUTManagerOFX** provides folder-backed LUT browsing for look management.

## Install

Run `scripts/INSTALL.command`, then refresh Resolve's DCTL/LUT list or restart Resolve.

## Releases

Every push/PR runs static validation. Push a `v*` tag to create a GitHub Release ZIP automatically.
