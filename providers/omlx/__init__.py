"""oMLX local provider exports."""

from providers.defaults import OMLX_DEFAULT_BASE

from .client import OmlxProvider

__all__ = [
    "OMLX_DEFAULT_BASE",
    "OmlxProvider",
]
