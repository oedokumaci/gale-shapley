# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v1.1.1](https://github.com/oedokumaci/gale-shapley/releases/tag/v1.1.1) - 2026-02-18

<small>[Compare with v1.1.0](https://github.com/oedokumaci/gale-shapley/compare/v1.1.0...v1.1.1)</small>

### Bug Fixes

- update hardcoded version test and resolve EncodingWarnings ([44509fb](https://github.com/oedokumaci/gale-shapley/commit/44509fbef7e9e8b88a6571ed62031fb071834b68) by oedokumaci).

## [v1.1.0](https://github.com/oedokumaci/gale-shapley/releases/tag/v1.1.0) - 2026-02-18

<small>[Compare with v1.0.0](https://github.com/oedokumaci/gale-shapley/compare/v1.0.0...v1.1.0)</small>

### Features

- add FastAPI backend and React frontend for GUI ([2e35e3a](https://github.com/oedokumaci/gale-shapley/commit/2e35e3aca68f27e2ef719753a490e4b1cec1ff22) by oedokumaci).

### Code Refactoring

- convert to zero-dep library with tests and modern tooling ([9888b86](https://github.com/oedokumaci/gale-shapley/commit/9888b86616aebf31774168a7dc8551cc79aa2f2d) by oedokumaci).

## [v1.0.0](https://github.com/oedokumaci/gale-shapley/releases/tag/v1.0.0) - 2024-12-29

<small>[Compare with first commit](https://github.com/oedokumaci/gale-shapley/compare/f9f02679d80070752869147acf83323217fd81ab...v1.0.0)</small>

### Features

- pass cli args and config to container ([c5082b4](https://github.com/oedokumaci/gale-shapley/commit/c5082b4e8d8dd72385da7f2eb73f1930aa6db0d8) by oedokumaci).
- add rich logging to std_out and refactor ([5168a21](https://github.com/oedokumaci/gale-shapley/commit/5168a213198acfac3a7a34042bdaeb65d853c996) by oedokumaci).
- add number_of_simulations arg to make run ([f91375f](https://github.com/oedokumaci/gale-shapley/commit/f91375fb697f5607bed10bd3cbfbec7b586fe624) by oedokumaci).
- update dependencies ([a06feeb](https://github.com/oedokumaci/gale-shapley/commit/a06feeb9816c5e5393059d14447ce4211ca012c8) by oedokumaci).
- add override log user input ([458f507](https://github.com/oedokumaci/gale-shapley/commit/458f50734b2a1c1848e1b2513321bd3c27cc2ccd) by oedokumaci).
- add swap_sides cli option ([d288608](https://github.com/oedokumaci/gale-shapley/commit/d288608a40207d069b35922869ad6c929c810a54) by oedokumaci).
- custom deterministic input ([d742469](https://github.com/oedokumaci/gale-shapley/commit/d742469a578089b0af41d3ee4b90cdc8870a90f2) by oedokumaci).

### Bug Fixes

- workdir already changed ([44ca259](https://github.com/oedokumaci/gale-shapley/commit/44ca25973745218067f04d5062514b282a8b6bae) by oedokumaci).
- requirements ([945b99c](https://github.com/oedokumaci/gale-shapley/commit/945b99c670342eaca004799c601fabb0dfd609f5) by oedokumaci).
- avoid recursive calls ([fd68e0f](https://github.com/oedokumaci/gale-shapley/commit/fd68e0fcd81ab84df72e4fc2cc83998e06f88a7e) by oedokumaci).
- fixes the wrong logging with custom input if number_of_side does not match with input side a warning is produced in that case logger does not log the true number of persons in that side ([444ed37](https://github.com/oedokumaci/gale-shapley/commit/444ed37c3a0de3a2e15067aaf88b3f0b088e94a4) by oedokumaci).

### Code Refactoring

- rename config_parser.py to config.py ([87c1e29](https://github.com/oedokumaci/gale-shapley/commit/87c1e29e2094a8e04adbab89a9fa025803f452ac) by oedokumaci).
- no need to str wrap also change timer decorator precision to .4f ([86a6ec0](https://github.com/oedokumaci/gale-shapley/commit/86a6ec0b87e5b9f64a15269895b70014a084d4ff) by oral.ersoy.dokumaci).
- style prints ([aa9c3ad](https://github.com/oedokumaci/gale-shapley/commit/aa9c3ad3d7fa18bdf9b974f3348596e8eb53b812) by oedokumaci).
- add !r ([b0ed891](https://github.com/oedokumaci/gale-shapley/commit/b0ed891d45e34db28e39261215401d45f5808380) by oral.ersoy.dokumaci).

