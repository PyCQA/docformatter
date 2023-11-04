# Changelog

## [v1.7.5](https://github.com/PyCQA/docformatter/tree/v1.7.5) (2023-07-12)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.7.4...v1.7.5)

Features

- fix: not recognizing `yield` as a sphinx field name [\#254](https://github.com/PyCQA/docformatter/pull/254) ([weibullguy](https://github.com/weibullguy))

## [v1.7.4](https://github.com/PyCQA/docformatter/tree/v1.7.4) (2023-07-10)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.7.3...v1.7.4)

Bug Fixes

- fix: summary with back ticks and sphinx field names with periods [\#248](https://github.com/PyCQA/docformatter/pull/248) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update documentation link for metadata [\#247](https://github.com/PyCQA/docformatter/pull/247) ([icp1994](https://github.com/icp1994))
- test: split format tests into multiple files [\#246](https://github.com/PyCQA/docformatter/pull/246) ([weibullguy](https://github.com/weibullguy))

## [v1.7.3](https://github.com/PyCQA/docformatter/tree/v1.7.3) (2023-06-23)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.7.2...v1.7.3)

Bug Fixes

- fix: removing newline between Sphinx field lists [\#237](https://github.com/PyCQA/docformatter/pull/237) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: move changelog to tag workflow [\#233](https://github.com/PyCQA/docformatter/pull/233) ([weibullguy](https://github.com/weibullguy))

## [v1.7.2](https://github.com/PyCQA/docformatter/tree/v1.7.2) (2023-06-07)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.7.1...v1.7.2)

Bug Fixes

- fix: wrapping issues with reST directives, quoted URLs, and Sphinx field lists [\#219](https://github.com/PyCQA/docformatter/pull/219) ([weibullguy](https://github.com/weibullguy))

## [v1.7.1](https://github.com/PyCQA/docformatter/tree/v1.7.1) (2023-05-19)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.7.0...v1.7.1)

Features

- feat: support epytext style [\#211](https://github.com/PyCQA/docformatter/pull/211) ([weibullguy](https://github.com/weibullguy))
- feat: use tomllib for Python 3.11+ [\#208](https://github.com/PyCQA/docformatter/pull/208) ([weibullguy](https://github.com/weibullguy))
- feat: wrap Sphinx style long parameter descriptions [\#201](https://github.com/PyCQA/docformatter/pull/201) ([weibullguy](https://github.com/weibullguy))

Bug Fixes

- fix: improper wrapping of short anonymous hyperlnks [\#213](https://github.com/PyCQA/docformatter/pull/213) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- chore: update version strings [\#214](https://github.com/PyCQA/docformatter/pull/214) ([weibullguy](https://github.com/weibullguy))
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

- chore: add GH release badge [\#200](https://github.com/PyCQA/docformatter/pull/200) ([weibullguy](https://github.com/weibullguy))
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

Bug Fixes

- fix: update URL handling functions [\#152](https://github.com/PyCQA/docformatter/pull/152) ([weibullguy](https://github.com/weibullguy))

**Merged pull requests:**

- docs: clarify future arguments [\#168](https://github.com/PyCQA/docformatter/pull/168) ([weibullguy](https://github.com/weibullguy))
- chore: update GitHub action workflows [\#153](https://github.com/PyCQA/docformatter/pull/153) ([weibullguy](https://github.com/weibullguy))

## [v1.5.1](https://github.com/PyCQA/docformatter/tree/v1.5.1) (2022-12-16)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.5.0...v1.5.1)

## [v1.5.0](https://github.com/PyCQA/docformatter/tree/v1.5.0) (2022-08-19)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.4...v1.5.0)

## [v1.4](https://github.com/PyCQA/docformatter/tree/v1.4) (2020-12-27)

[Full Changelog](https://github.com/PyCQA/docformatter/compare/v1.3.1...v1.4)



