"""
mftool_wrappers
---------------

Wrapper classes around the `mftool` library for easier and structured access:
- MFClient   : Low-level API client
- MFRegistry : Registry of all available schemes
- MFScheme   : Representation of a single mutual fund scheme
"""

from .client import MFClient
from .registry import MFRegistry
from .scheme import MFScheme

__all__ = ["MFClient", "MFRegistry", "MFScheme"]
