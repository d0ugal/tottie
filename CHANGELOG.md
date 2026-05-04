# Changelog

## [0.5.0](https://github.com/d0ugal/tottie/compare/v0.4.0...v0.5.0) (2026-05-04)


### Features

* add position parameter to text overlay functions ([77cb6b6](https://github.com/d0ugal/tottie/commit/77cb6b655e302e1d22079cab1f16777289939c76))
* configurable background dim on text overlay ([38c1c82](https://github.com/d0ugal/tottie/commit/38c1c8240a57ed5ed46afb8d4eb82d031907d75d))


### Bug Fixes

* per-line text backgrounds and improved N glyph ([fdb82e2](https://github.com/d0ugal/tottie/commit/fdb82e28115c7d0f5022ce2b37b315f5a0fb1b70))
* use ternary for y0 assignment to satisfy ruff SIM108 ([5bafa41](https://github.com/d0ugal/tottie/commit/5bafa41fca0f4eefa8590d57852b1d6c96f4bbec))

## [0.4.0](https://github.com/d0ugal/tottie/compare/v0.3.0...v0.4.0) (2026-04-21)


### Features

* move corner char to bottom-right, scale to 2×2 pixels ([bd262f3](https://github.com/d0ugal/tottie/commit/bd262f35d310ab765dda89131f09ba121022802c))

## [0.3.0](https://github.com/d0ugal/tottie/compare/v0.2.1...v0.3.0) (2026-04-21)


### Features

* add apply_corner_char for bottom-left single-glyph overlay ([3db4281](https://github.com/d0ugal/tottie/commit/3db4281ce01cb9909da2fd019ea238d796cd0c0d))

## [0.2.1](https://github.com/d0ugal/tottie/compare/v0.2.0...v0.2.1) (2026-04-16)


### Bug Fixes

* restore missing blank lines between import groups in tests ([e1cc257](https://github.com/d0ugal/tottie/commit/e1cc25732d4a6ba382c0436b016ba83a9371c8ef))


### Performance Improvements

* vectorise to_rgb565 with NumPy ([607a0ed](https://github.com/d0ugal/tottie/commit/607a0ed2327cd0b0a84bd0fc87170ee760e2dde6))

## [0.2.0](https://github.com/d0ugal/tottie/compare/v0.1.1...v0.2.0) (2026-04-10)


### Features

* add anchor parameter to crop_and_resize for off-centre crops ([4311f17](https://github.com/d0ugal/tottie/commit/4311f17809562eb2d3ae9029786dc30a16ee97e0))

## [0.1.1](https://github.com/d0ugal/tottie/compare/v0.1.0...v0.1.1) (2026-04-07)


### Bug Fixes

* resolve pyright type errors in moon, overlay, and tests ([d43341c](https://github.com/d0ugal/tottie/commit/d43341ca99997618d7aa8e06ed3f2311c0a34f6c))
