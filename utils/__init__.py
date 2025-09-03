"""
    utils
    ------

    The `utils` package provides utility modules for data loading, formatting, and chart plotting to support the invest_tracker application. These utilities are designed to be reusable, modular, and easy to maintain, following best practices for Python package development.

    Modules
    -------

    - `data_loader`: Functions and classes for loading and processing data from various sources.
    - `formatters`: Utilities for formatting data, such as dates, numbers, and strings, for display or further processing.

    Usage
    -----

    Import the required utility module as follows::

        from utils import data_loader, formatters

    or import specific functions/classes from a module::

        from utils.data_loader import BlacklistManager, FavouritesManager, SimulationManager, MyInvestmentsManager
        from utils.formatters import reorder_and_format_dict
    Conventions
    -----------

    - All modules are self-contained and do not have side effects on import.
    - Each module includes its own documentation and follows PEP 8 style guidelines.
    - The package is intended for internal use within the invest_tracker project, but modules are written to be reusable.

    Author: Abhinav Singla
    Created: August 2025
    License: MIT
"""

__all__ = [
    'data_loader',
    'formatters',
    'gcs_client'
]


