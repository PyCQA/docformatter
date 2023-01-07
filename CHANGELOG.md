# Changelog

## [v1.5.1](https://github.com/PyCQA/docformatter/tree/v1.5.1) (2022-12-16)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.5.0...v1.5.1)

Bug Fixes

- Fix incorrect pyproject.toml parsing of boolean values [\#133](https://github.com/PyCQA/docformatter/pull/133) ([weibullguy](https://github.com/weibullguy))
- fix: don't wrap URLs [\#115](https://github.com/PyCQA/docformatter/pull/115) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update CI workflow so 3.6 still runs [\#132](https://github.com/PyCQA/docformatter/pull/132) ([weibullguy](https://github.com/weibullguy))
- No empty lines before class and method docstrings [\#131](https://github.com/PyCQA/docformatter/pull/131) ([mcflugen](https://github.com/mcflugen))
- Allow showing the diff when using --in-place or --check with --diff [\#128](https://github.com/PyCQA/docformatter/pull/128) ([BenjaminSchubert](https://github.com/BenjaminSchubert))
- chore: move script to src layout and make a package [\#117](https://github.com/PyCQA/docformatter/pull/117) ([weibullguy](https://github.com/weibullguy))
- feat: format class attribute docstrings [\#116](https://github.com/PyCQA/docformatter/pull/116) ([weibullguy](https://github.com/weibullguy))
- refactor: move encoding/decoding functions to encodor class [\#111](https://github.com/PyCQA/docformatter/pull/111) ([weibullguy](https://github.com/weibullguy))
- refactor: move functions to classes [\#110](https://github.com/PyCQA/docformatter/pull/110) ([weibullguy](https://github.com/weibullguy))

## [v1.5.0](https://github.com/PyCQA/docformatter/tree/v1.5.0) (2022-08-19)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.4...v1.5.0)

**Merged pull requests:**

- chore: add workflow actions [\#108](https://github.com/PyCQA/docformatter/pull/108) ([weibullguy](https://github.com/weibullguy))
- feat: adjust for tab when wrapping [\#105](https://github.com/PyCQA/docformatter/pull/105) ([weibullguy](https://github.com/weibullguy))
- feat: add option to place closing quotes on newline [\#104](https://github.com/PyCQA/docformatter/pull/104) ([weibullguy](https://github.com/weibullguy))
- test: move remaining tests to tests/ directory [\#102](https://github.com/PyCQA/docformatter/pull/102) ([weibullguy](https://github.com/weibullguy))
- feat: add support for setup.cfg and tox.ini configuration files [\#101](https://github.com/PyCQA/docformatter/pull/101) ([weibullguy](https://github.com/weibullguy))
- fix: definitions corrupted with in-line comment [\#99](https://github.com/PyCQA/docformatter/pull/99) ([weibullguy](https://github.com/weibullguy))
- fix: remove empty line [\#96](https://github.com/PyCQA/docformatter/pull/96) ([weibullguy](https://github.com/weibullguy))
- chore: update README [\#95](https://github.com/PyCQA/docformatter/pull/95) ([weibullguy](https://github.com/weibullguy))
- fix: add argument to turn on/off many lines of short words being a list [\#93](https://github.com/PyCQA/docformatter/pull/93) ([weibullguy](https://github.com/weibullguy))
- fix: add support for raw and unicode docstrings [\#91](https://github.com/PyCQA/docformatter/pull/91) ([weibullguy](https://github.com/weibullguy))
- test: move tests to directory [\#90](https://github.com/PyCQA/docformatter/pull/90) ([weibullguy](https://github.com/weibullguy))
- build: Add pyproject.toml for docformatter repository [\#88](https://github.com/PyCQA/docformatter/pull/88) ([weibullguy](https://github.com/weibullguy))
- fix: Don't format lines beginning with single quotes [\#87](https://github.com/PyCQA/docformatter/pull/87) ([weibullguy](https://github.com/weibullguy))
- build: Add optional tomli dependency to setup.py [\#86](https://github.com/PyCQA/docformatter/pull/86) ([weibullguy](https://github.com/weibullguy))
- Switch to Github Actions from Travis-CI, update supported python version [\#80](https://github.com/PyCQA/docformatter/pull/80) ([asherf](https://github.com/asherf))
- Add pyproject.toml support for config \(Issue \#10\) [\#77](https://github.com/PyCQA/docformatter/pull/77) ([weibullguy](https://github.com/weibullguy))
- Bugfix --wrap-summaries 0 now fully disables summary wrapping [\#74](https://github.com/PyCQA/docformatter/pull/74) ([howeaj](https://github.com/howeaj))
- Better document --docstring-length option and add it to the readme [\#72](https://github.com/PyCQA/docformatter/pull/72) ([AntoineD](https://github.com/AntoineD))
- Removed the empty line between function definition and docstring \#51 [\#53](https://github.com/PyCQA/docformatter/pull/53) ([dabauxi](https://github.com/dabauxi))
- Pre-Summary Space Option [\#46](https://github.com/PyCQA/docformatter/pull/46) ([alecmerdler](https://github.com/alecmerdler))

## [v1.4](https://github.com/PyCQA/docformatter/tree/v1.4) (2020-12-27)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.3.1...v1.4)

**Merged pull requests:**

- Add --docstring-length flag [\#63](https://github.com/PyCQA/docformatter/pull/63) ([Pacu2](https://github.com/Pacu2))
- Not add period for summary formatted as title [\#57](https://github.com/PyCQA/docformatter/pull/57) ([lli-fincad](https://github.com/lli-fincad))
- Documentation on integrating docformatter with git and PyCharm [\#50](https://github.com/PyCQA/docformatter/pull/50) ([OliverSieweke](https://github.com/OliverSieweke))
- Added command line exclude option [\#44](https://github.com/PyCQA/docformatter/pull/44) ([dabauxi](https://github.com/dabauxi))



