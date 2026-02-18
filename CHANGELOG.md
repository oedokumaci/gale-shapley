# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v1.2.0](https://github.com/oedokumaci/gale-shapley-algorithm/releases/tag/v1.2.0) - 2026-02-18

<small>[Compare with v1.1.3](https://github.com/oedokumaci/gale-shapley-algorithm/compare/v1.1.3...v1.2.0)</small>

### Features

- replace YAML config CLI with interactive terminal prompts ([7d3d742](https://github.com/oedokumaci/gale-shapley-algorithm/commit/7d3d742) by oedokumaci).
- add algorithm explainer, randomize button, and polish SVG layout ([9f38fa6](https://github.com/oedokumaci/gale-shapley-algorithm/commit/9f38fa6) by oedokumaci).
- replace text-based animation with SVG visualization and celebrity defaults ([2d74fd1](https://github.com/oedokumaci/gale-shapley-algorithm/commit/2d74fd1) by oedokumaci).

### Bug Fixes

- fix Docker build and serve frontend from FastAPI ([6741e1d](https://github.com/oedokumaci/gale-shapley-algorithm/commit/6741e1d) by oedokumaci).

### Code Refactoring

- address PR review findings ([39e2858](https://github.com/oedokumaci/gale-shapley-algorithm/commit/39e2858) by oedokumaci).

## [v1.1.3](https://github.com/oedokumaci/gale-shapley-algorithm/releases/tag/v1.1.3) - 2026-02-18

<small>[Compare with v1.1.2](https://github.com/oedokumaci/gale-shapley-algorithm/compare/v1.1.2...v1.1.3)</small>

### Fixed

- fix: add missing shadcn/ui utility needed by frontend components ([f444af3](https://github.com/oedokumaci/gale-shapley-algorithm/commit/f444af30a3fd98f9a51e6c2d01a5b47314007de1) by oedokumaci).

## [v1.1.2](https://github.com/oedokumaci/gale-shapley-algorithm/releases/tag/v1.1.2) - 2026-02-18

<small>[Compare with v1.1.1](https://github.com/oedokumaci/gale-shapley-algorithm/compare/v1.1.1...v1.1.2)</small>

## [v1.1.1](https://github.com/oedokumaci/gale-shapley-algorithm/releases/tag/v1.1.1) - 2026-02-18

<small>[Compare with v1.1.0](https://github.com/oedokumaci/gale-shapley-algorithm/compare/v1.1.0...v1.1.1)</small>

### Fixed

- fix: update hardcoded version test and resolve EncodingWarnings ([44509fb](https://github.com/oedokumaci/gale-shapley-algorithm/commit/44509fbef7e9e8b88a6571ed62031fb071834b68) by oedokumaci).

## [v1.1.0](https://github.com/oedokumaci/gale-shapley-algorithm/releases/tag/v1.1.0) - 2026-02-18

<small>[Compare with v1.0.0](https://github.com/oedokumaci/gale-shapley-algorithm/compare/v1.0.0...v1.1.0)</small>

## [v1.0.0](https://github.com/oedokumaci/gale-shapley-algorithm/releases/tag/v1.0.0) - 2024-12-29

<small>[Compare with first commit](https://github.com/oedokumaci/gale-shapley-algorithm/compare/f9f02679d80070752869147acf83323217fd81ab...v1.0.0)</small>

### Added

- Add utils.py with timer_decorator ([4e3eb5c](https://github.com/oedokumaci/gale-shapley-algorithm/commit/4e3eb5c7e10b24fc8d175728994b708b7d2d774e) by oral.ersoy.dokumaci).
- Add jupyter notebooks ([4b4eddc](https://github.com/oedokumaci/gale-shapley-algorithm/commit/4b4eddcd8618caf8bd650cbd6b1879cc64f50079) by oral.ersoy.dokumaci).
- Add new picture to readme ([9709dc0](https://github.com/oedokumaci/gale-shapley-algorithm/commit/9709dc0a26968e27a9e45e01f3fd7d085d82e537) by oral.ersoy.dokumaci).
- Add Simulator class remove create_objects.py ([5c6a5d6](https://github.com/oedokumaci/gale-shapley-algorithm/commit/5c6a5d6248fbc8bee07fc723958a1480ec66e8b3) by oral.ersoy.dokumaci).
- Add docstrings and add create_objects.py ([4dc5b42](https://github.com/oedokumaci/gale-shapley-algorithm/commit/4dc5b42bd2a667c574d6e758764a4e2013be5287) by oral.ersoy.dokumaci).
- Add jupytext outputs These auto add when open as jupyter notebook ([a2171d0](https://github.com/oedokumaci/gale-shapley-algorithm/commit/a2171d0d915fe5d5922b10230b756528e3cb073e) by oral.ersoy.dokumaci).
- Add Proposer and Responder classes (subclasses of Person) ([5ac896b](https://github.com/oedokumaci/gale-shapley-algorithm/commit/5ac896b7246a5fb75ed296aea1155873da6f553e) by oral.ersoy.dokumaci).
- Added jupyter notebooks to gitignore ([451569c](https://github.com/oedokumaci/gale-shapley-algorithm/commit/451569c95a86434f32d3debd7e82b252adfbbe98) by oedokumaci).

### Fixed

- fix: workdir already changed ([44ca259](https://github.com/oedokumaci/gale-shapley-algorithm/commit/44ca25973745218067f04d5062514b282a8b6bae) by oedokumaci).
- fix: requirements ([945b99c](https://github.com/oedokumaci/gale-shapley-algorithm/commit/945b99c670342eaca004799c601fabb0dfd609f5) by oedokumaci).
- fix: avoid recursive calls ([fd68e0f](https://github.com/oedokumaci/gale-shapley-algorithm/commit/fd68e0fcd81ab84df72e4fc2cc83998e06f88a7e) by oedokumaci).
- fix: fixes the wrong logging with custom input if number_of_side does not match with input side a warning is produced in that case logger does not log the true number of persons in that side ([444ed37](https://github.com/oedokumaci/gale-shapley-algorithm/commit/444ed37c3a0de3a2e15067aaf88b3f0b088e94a4) by oedokumaci).
- Fix logs directory error at initalization Fixes #7 ([f0d68d6](https://github.com/oedokumaci/gale-shapley-algorithm/commit/f0d68d655b0a198488043362dc8dae83d06c5a3f) by oedokumaci).
- Fix string.casefold instead of string.lower ([2c65d79](https://github.com/oedokumaci/gale-shapley-algorithm/commit/2c65d794d53c21b25928f4731b1b3c7a625328e8) by oedokumaci).
- Fix case sensitive input problem Also add compact keyword argument to run methods Also change acceptable preference type name to Random ([2069427](https://github.com/oedokumaci/gale-shapley-algorithm/commit/206942757613333211cd21c679d65676f7bf4965) by oedokumaci).
- Fix for both posix and windows paths Fixes #2 ([8812961](https://github.com/oedokumaci/gale-shapley-algorithm/commit/88129615b5f3f66affbe68d49b84039462fbb7b4) by oedokumaci).
- Fixes #1 ([57811a5](https://github.com/oedokumaci/gale-shapley-algorithm/commit/57811a52735255214d7e2d97423c0e3c4724542d) by oedokumaci).
- Fix TwoSidedMatchingError is not used ([e44e41d](https://github.com/oedokumaci/gale-shapley-algorithm/commit/e44e41d24b81c1b45a7ec1f127b283bbcde4d721) by oedokumaci).
- Fix tests in accordance with pydantic Also uncomment pytest pre-commit ([c503732](https://github.com/oedokumaci/gale-shapley-algorithm/commit/c503732ca301b196abd77c8f72f7b95cce5d4ade) by oral.ersoy.dokumaci).
- Fix type safety move proposer_responder to person Also add gale.shapley to imports ([a3688cc](https://github.com/oedokumaci/gale-shapley-algorithm/commit/a3688ccff43d1650fce4b1764762ed07ce25cba6) by oral.ersoy.dokumaci).
- Fix add gale_shapley. to imports ([32480ec](https://github.com/oedokumaci/gale-shapley-algorithm/commit/32480ec09c2df99f37188597e129e9fe2b97adf5) by oral.ersoy.dokumaci).
- Fix import logging directly ([d594955](https://github.com/oedokumaci/gale-shapley-algorithm/commit/d5949552f70a2665699f643dec4aa394bfed836f) by oral.ersoy.dokumaci).
- Fix logs path ([64bcb2b](https://github.com/oedokumaci/gale-shapley-algorithm/commit/64bcb2b19237a69b02edab3ad563fcf8fd5ff624) by oral.ersoy.dokumaci).
- Fix call run method with new simulate name ([a2d5cc5](https://github.com/oedokumaci/gale-shapley-algorithm/commit/a2d5cc567a93fa068ba62425b9a8d7d86f9a0435) by oral.ersoy.dokumaci).
- Fix missing return statement Also add and update docstrings ([46ae963](https://github.com/oedokumaci/gale-shapley-algorithm/commit/46ae963af9ac2e9cc46e33383d0bbdca066b3c96) by oral.ersoy.dokumaci).
- Fix there is a method for that ([3c88173](https://github.com/oedokumaci/gale-shapley-algorithm/commit/3c881733741435ca9dcf070c4fd623807f64c80d) by oral.ersoy.dokumaci).
- Fix unequal number of proposers and responders ([2f65704](https://github.com/oedokumaci/gale-shapley-algorithm/commit/2f657049e240345e07077faf6db55f4e50954d6f) by oral.ersoy.dokumaci).
- Fix print_all_preferences bug Feat make compact printing default ([a09fd72](https://github.com/oedokumaci/gale-shapley-algorithm/commit/a09fd721578ee0a36f7a89aa41a1864216af66e1) by oral.ersoy.dokumaci).
- Fix is_acceptable not public anymore ([69e5d28](https://github.com/oedokumaci/gale-shapley-algorithm/commit/69e5d28a84cca9681157cd3e1cddffa77ab5d39e) by oral.ersoy.dokumaci).
- Fix make is_acceptable public ([0efdbb7](https://github.com/oedokumaci/gale-shapley-algorithm/commit/0efdbb7be549b3b102cc6638ba862c010f6f44d7) by oral.ersoy.dokumaci).
- Fix round __slot__ ([2048544](https://github.com/oedokumaci/gale-shapley-algorithm/commit/20485440a1b41b1c4ed375a878fa37709ac6b77a) by oral.ersoy.dokumaci).
- Fix unused SideNameError exception ([6b89c37](https://github.com/oedokumaci/gale-shapley-algorithm/commit/6b89c37f516aa7521732d1f3a461507400e8037f) by oral.ersoy.dokumaci).
- Fix no need for yaml in person.py ([2c75d2d](https://github.com/oedokumaci/gale-shapley-algorithm/commit/2c75d2d0138716fbf91f4bb3f0c89f78443b18dc) by oral.ersoy.dokumaci).
- Fix error super class is specific ([57ea897](https://github.com/oedokumaci/gale-shapley-algorithm/commit/57ea8977b7133b4ff64319bc04e128100e77d16e) by oral.ersoy.dokumaci).

