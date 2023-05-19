# Changelog

## [Unreleased](https://github.com/PyCQA/docformatter/tree/HEAD)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.7.0...HEAD)

Features

- feat: use tomllib for Python 3.11+ [\#208](https://github.com/PyCQA/docformatter/pull/208) ([weibullguy](https://github.com/weibullguy))
- feat: wrap Sphinx style long parameter descriptions [\#201](https://github.com/PyCQA/docformatter/pull/201) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update pre-commit-config [\#209](https://github.com/PyCQA/docformatter/pull/209) ([weibullguy](https://github.com/weibullguy))

## [v1.7.0](https://github.com/PyCQA/docformatter/tree/v1.7.0) (2023-05-15)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.6.5...v1.7.0)

Features

- feat: add option to format compatible with black [\#196](https://github.com/PyCQA/docformatter/pull/196) ([weibullguy](https://github.com/weibullguy))
- feat: add option for user to provide list of words not to capitalize [\#195](https://github.com/PyCQA/docformatter/pull/195) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update workflows [\#206](https://github.com/PyCQA/docformatter/pull/206) ([weibullguy](https://github.com/weibullguy))

## [v1.6.5](https://github.com/PyCQA/docformatter/tree/v1.6.5) (2023-05-03)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.6.4...v1.6.5)

Bug Fixes

- fix: removing blank line after import section [\#204](https://github.com/PyCQA/docformatter/pull/204) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update workflows to create release [\#198](https://github.com/PyCQA/docformatter/pull/198) ([weibullguy](https://github.com/weibullguy))
- chore: update GH actions to generate CHANGELOG [\#194](https://github.com/PyCQA/docformatter/pull/194) ([weibullguy](https://github.com/weibullguy))

## [v1.6.4](https://github.com/PyCQA/docformatter/tree/v1.6.4) (2023-04-26)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.6.3...v1.6.4)

Bug Fixes

- fix: IndexError when only URL in long description [\#190](https://github.com/PyCQA/docformatter/pull/190) ([weibullguy](https://github.com/weibullguy))
- fix: removing newline after shebang [\#188](https://github.com/PyCQA/docformatter/pull/188) ([weibullguy](https://github.com/weibullguy))
- fix: not capitalizing first word when summary ends in period [\#185](https://github.com/PyCQA/docformatter/pull/185) ([weibullguy](https://github.com/weibullguy))

## [v1.6.3](https://github.com/PyCQA/docformatter/tree/v1.6.3) (2023-04-23)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.6.2...v1.6.3)

Bug Fixes

- fix: adding newlines around wrapped URL [\#182](https://github.com/PyCQA/docformatter/pull/182) ([weibullguy](https://github.com/weibullguy))
- fix: adding blank line in summary with symbol [\#179](https://github.com/PyCQA/docformatter/pull/179) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- ci: split test suite run into unit and system [\#181](https://github.com/PyCQA/docformatter/pull/181) ([weibullguy](https://github.com/weibullguy))

## [v1.6.2](https://github.com/PyCQA/docformatter/tree/v1.6.2) (2023-04-22)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.6.1...v1.6.2)

Bug Fixes

- fix: remove blank after comment [\#177](https://github.com/PyCQA/docformatter/pull/177) ([weibullguy](https://github.com/weibullguy))

## [v1.6.1](https://github.com/PyCQA/docformatter/tree/v1.6.1) (2023-04-21)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.6.0...v1.6.1)

Bug Fixes

- fix: remove blank lines after line beginning with 'def' [\#171](https://github.com/PyCQA/docformatter/pull/171) ([weibullguy](https://github.com/weibullguy))

## [v1.6.0](https://github.com/PyCQA/docformatter/tree/v1.6.0) (2023-04-04)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.5.1...v1.6.0)

Features

- \(🎁\) Support python 3.11 [\#164](https://github.com/PyCQA/docformatter/pull/164) ([KotlinIsland](https://github.com/KotlinIsland))
- feat: add file config options [\#137](https://github.com/PyCQA/docformatter/pull/137) ([weibullguy](https://github.com/weibullguy))

Bug Fixes

- fix: update URL handling functions [\#152](https://github.com/PyCQA/docformatter/pull/152) ([weibullguy](https://github.com/weibullguy))
- fix: add additional URL patterns [\#148](https://github.com/PyCQA/docformatter/pull/148) ([weibullguy](https://github.com/weibullguy))
- fix: wrap multi-paragraph long descriptions [\#143](https://github.com/PyCQA/docformatter/pull/143) ([weibullguy](https://github.com/weibullguy))
- fix: handle blank lines after class definition properly [\#142](https://github.com/PyCQA/docformatter/pull/142) ([weibullguy](https://github.com/weibullguy))
- fix: handle index error in link wrapping [\#141](https://github.com/PyCQA/docformatter/pull/141) ([weibullguy](https://github.com/weibullguy))
- fix: remove blank line after method docstring [\#138](https://github.com/PyCQA/docformatter/pull/138) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- docs: clarify future arguments [\#168](https://github.com/PyCQA/docformatter/pull/168) ([weibullguy](https://github.com/weibullguy))
- chore: update GitHub action workflows [\#153](https://github.com/PyCQA/docformatter/pull/153) ([weibullguy](https://github.com/weibullguy))
- chore: drop support for Python3.6 [\#149](https://github.com/PyCQA/docformatter/pull/149) ([weibullguy](https://github.com/weibullguy))
- docs: fix typos [\#147](https://github.com/PyCQA/docformatter/pull/147) ([kianmeng](https://github.com/kianmeng))
- chore: create do-release workflow [\#135](https://github.com/PyCQA/docformatter/pull/135) ([weibullguy](https://github.com/weibullguy))

## [v1.5.1](https://github.com/PyCQA/docformatter/tree/v1.5.1) (2022-12-16)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.5.0...v1.5.1)

Features

- feat: format class attribute docstrings [\#116](https://github.com/PyCQA/docformatter/pull/116) ([weibullguy](https://github.com/weibullguy))

Bug Fixes

- Fix incorrect pyproject.toml parsing of boolean values [\#133](https://github.com/PyCQA/docformatter/pull/133) ([weibullguy](https://github.com/weibullguy))
- fix: don't wrap URLs [\#115](https://github.com/PyCQA/docformatter/pull/115) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update CI workflow so 3.6 still runs [\#132](https://github.com/PyCQA/docformatter/pull/132) ([weibullguy](https://github.com/weibullguy))
- No empty lines before class and method docstrings [\#131](https://github.com/PyCQA/docformatter/pull/131) ([mcflugen](https://github.com/mcflugen))
- Allow showing the diff when using --in-place or --check with --diff [\#128](https://github.com/PyCQA/docformatter/pull/128) ([BenjaminSchubert](https://github.com/BenjaminSchubert))
- chore: move script to src layout and make a package [\#117](https://github.com/PyCQA/docformatter/pull/117) ([weibullguy](https://github.com/weibullguy))
- refactor: move encoding/decoding functions to encodor class [\#111](https://github.com/PyCQA/docformatter/pull/111) ([weibullguy](https://github.com/weibullguy))
- refactor: move functions to classes [\#110](https://github.com/PyCQA/docformatter/pull/110) ([weibullguy](https://github.com/weibullguy))

## [v1.5.0](https://github.com/PyCQA/docformatter/tree/v1.5.0) (2022-08-19)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.4...v1.5.0)

**Merged pull requests:**

- chore: add workflow actions [\#108](https://github.com/PyCQA/docformatter/pull/108) ([weibullguy](https://github.com/weibullguy))

## [v1.4](https://github.com/PyCQA/docformatter/tree/v1.4) (2020-12-27)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.3.1...v1.4)



