"""9routor local proxy provider exports."""

from providers.defaults import NINEROUTER_DEFAULT_BASE

from .client import NineRouterProvider

__all__ = [
    "NINEROUTER_DEFAULT_BASE",
    "NineRouterProvider",
]
