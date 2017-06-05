# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.0.0] - 2017-06-04
### Added
- Command line interface.
- Config class to manage cucco configuration and handle normalizations. This class allows to load normalizations to apply from a yaml file.
- Debug log messages to see what -the cucco- is happening behind the scenes.

### Changed
- Order of default normalizations to remove extra white spaces after removing punctuation.

## [1.1.0] - 2017-05-15
### Changed
- New stop words files. Cucco is hungry for words and now can deal with 50 laguages.
