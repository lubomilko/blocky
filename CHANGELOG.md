# Changelog

[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

---

This file documents all notable changes in the [blocky](https://github.com/lubomilko/blocky)
template engine project.

---


## [unreleased] - 202y-mm-dd

*Changes for the upcoming new version.*


## [1.4.0] - 2025-03-30

### Added

- Add a possibility to clear variables by setting them to `None` or `{}` when filling the
  template using the `fill()` method.


## [1.3.0] - 2025-03-29

### Added

- Add possibility to fill multiple blocks with the same name, but different template to be
  filled by the `fill()` method, instead of setting the same filled content into all blocks
  with the same name.
- Add option to set the template block by the `fill()` method using any non-empty string,
  non-zero or true value assigned directly to the block's dictionary or object attribute.
  Alternatively, a block can be cleared by setting it to an empty string, zero or false value.


## [1.2.0] - 2025-03-03

### Added

- Add support for a new optional attribute `vari_idx` in a dictionary or object used as a
  `block_data` input to the `fill()` method. The new attribute can define the `variation_idx`
  attribute of the `set()` method used for setting the parent block containing the attribute into
  the template.


## [1.1.2] - 2025-02-08

### Fixed

- Add protection against endless while loops in `set()` and `__set_std_last_first_tag` methods.


## [1.1.1] - 2025-02-08

### Fixed

- Fix condition for filling object or dictionary values into the template tags in the `fill()` method.


## [1.1.0] - 2025-01-19

### Added

- Add option to fill the template using a data defined by a dictionary.
- Add option to set multiple subblocks at once using their names instead of providing the subblock
  objects.
- Add option to clear a single block using by the `set()` method with a `variation_idx` set to a
  negative or `False` value. 


## [1.0.0] - 2024-01-05

*Initial open-source version based on the previously proprietary module blocky 3.5.0.*


[unreleased]: https://github.com/lubomilko/blocky
[1.4.0]: https://github.com/lubomilko/blocky/releases/tag/1.4.0
[1.3.0]: https://github.com/lubomilko/blocky/releases/tag/1.3.0
[1.2.0]: https://github.com/lubomilko/blocky/releases/tag/1.2.0
[1.1.2]: https://github.com/lubomilko/blocky/releases/tag/1.1.2
[1.1.1]: https://github.com/lubomilko/blocky/releases/tag/1.1.1
[1.1.0]: https://github.com/lubomilko/blocky/releases/tag/1.1.0
[1.0.0]: https://github.com/lubomilko/blocky/releases/tag/1.0.0
