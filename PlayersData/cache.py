from functools import wraps
from collections.abc import Iterable


# from burnysc2
def cache_once_per_frame(f):
    """
    This decorator caches the return value for one game loop,
    then clears it if it is accessed in a different game loop.
    """

    @wraps(f)
    def inner(self, *args, **kwargs):
        property_cache = "_cache_" + f.__name__
        state_cache = "_frame_" + f.__name__
        cache_updated = getattr(self, state_cache, -1) == self._bot.state.game_loop
        if not cache_updated:
            setattr(self, property_cache, f(self, *args, **kwargs))
            setattr(self, state_cache, 1)
        cache = getattr(self, property_cache)
        should_copy = callable(getattr(cache, "copy", None))
        if should_copy:
            return cache.copy()
        return cache
    return inner


def property_cache_once_per_frame(f):
    """
    This decorator caches the return value for one game loop,
    then clears it if it is accessed in a different game loop.
    """

    @wraps(f)
    def inner(self):
        property_cache = "_cache_" + f.__name__
        state_cache = "_frame_" + f.__name__
        cache_updated = getattr(self, state_cache, -1) == self._bot.state.game_loop
        if not cache_updated:
            setattr(self, property_cache, f(self))
            setattr(self, state_cache, self._bot.state.game_loop)

        cache = getattr(self, property_cache)
        should_copy = callable(getattr(cache, "copy", None))
        if should_copy:
            return cache.copy()
        return cache

    return property(inner)
