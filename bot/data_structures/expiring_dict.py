from .expiring_mixin import ExpiringMixin
from collections import UserDict


class ExpiringDict(ExpiringMixin, UserDict):
    pass
