# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] 2025-03-02 - Add Dhamma Talks data collection

### Added

1. Data collection
    1. Added `data_collector.py` to define the API for data collectors and define shared functionality
    2. Added `dhamma_talks.py` to scrape Dhamma Talks website for sutta references.
    3. Added notebook `2025_03_02_Collect_Data_From_Dhamma_Talks.ipynb` to call the `dhamma_talks.py` data collection.
2. General utility classes
    1. Added `config.py` to hold config data
    2. Added `logger.py` to hold useful, shared logging logic


### Changed

1. Project configuration
    1. Updated dependencies to include beautifulsoup4 and pandas for web scraping.
    2. Added data directory to .gitignore.


## [0.0.1] 2025-01-24 - Project Setup

### Added

1. Python project setup code
    1. Pyproject.toml to manage project dependencies.
    2. `scripture_search/main.py` as a placeholder.
    3. `tests/test_main.py` as a placeholder test.
2. Project management stuff
    1. Changelog to track changes in the project.
    2. Pull Request template to guide contributors.
    3. Added planning folder to hold planning documents for the project.
    4. Added `2025-01-25_ideation.md` to track initial ideation for the project.
3. GitHub Actions
    1. Code check action - runs pylint, black, and pytest (with coverage).
