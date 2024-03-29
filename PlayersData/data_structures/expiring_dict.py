from threading import RLock
from typing import TYPE_CHECKING, Iterable, Union

if TYPE_CHECKING:
    from sc2.bot_ai import BotAI


# Copied from python-sc2 with some changes


class ExpiringDict(dict):
    """
    An expiring dict that uses the bot.state.game_loop to only return items that are valid for a specific amount of time.

    Example usages::

        async def on_step(iteration: int):
            # This dict will hold up to 10 items and only return values that have been added up to 20 frames ago
            my_dict = ExpiringDict(self, max_age_frames=20)
            if iteration == 0:
                # Add item
                my_dict["test"] = "something"
            if iteration == 2:
                # On default, one iteration is called every 8 frames
                if "test" in my_dict:
                    print("test is in dict")
            if iteration == 20:
                if "test" not in my_dict:
                    print("test is not anymore in dict")
    """

    def __init__(self, bot: "BotAI", max_age_frames: int = 1):
        super().__init__()
        assert max_age_frames >= -1
        assert bot

        self.bot: BotAI = bot
        self.max_age: Union[int, float] = max_age_frames
        self.lock: RLock = RLock()

    @property
    def frame(self) -> int:
        return self.bot.state.game_loop

    def __contains__(self, key) -> bool:
        """ Return True if dict has key, else False, e.g. 'key in dict' """
        with self.lock:
            if dict.__contains__(self, key):
                # Each item is a list of [value, frame time]
                item = dict.__getitem__(self, key)
                if self.frame - item[1] < self.max_age:
                    return True
                else:
                    del self[key]
        return False

    def __getitem__(self, key, with_age=False) -> any:
        """ Return the item of the dict using d[key] """
        with self.lock:
            try:
                # Each item is a list of [value, frame time]
                item = dict.__getitem__(self, key)
                if self.frame - item[1] < self.max_age:
                    if with_age:
                        return item[0], item[1]
                    return item[0]
                else:
                    del self[key]
            except:
                pass
        raise KeyError(key)

    def __setitem__(self, key, value):
        """ Set d[key] = value """
        with self.lock:
            dict.__setitem__(self, key, (value, self.frame))

    def __repr__(self):
        """ Printable version of the dict instead of getting memory adress """
        print_list = []
        with self.lock:
            for key, value in dict.items(self):
                if self.frame - value[1] < self.max_age:
                    try:
                        print_list.append(f"{repr(key)}: {repr(value)}")
                    except:
                        print_list.append(f"{key}: {value}")
        print_str = ", ".join(print_list)
        return f"ExpiringDict({print_str})"

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        """ Override 'for key in dict:' """
        with self.lock:
            return self.keys()

    def __len__(self):
        """Override len method as key value pairs aren't instantly being deleted, but only on __get__(item).
        This function is slow because it has to check if each element is not expired yet."""
        with self.lock:
            count = 0
            for _ in self.values():
                count += 1
            return count

    # TODO find a way to improve len
    def pop(self, key, default=None, with_age=False):
        """ Return the item and remove it """
        with self.lock:
            if dict.__contains__(self, key):
                item = dict.__getitem__(self, key)
                if self.frame - item[1] < self.max_age:
                    del self[key]
                    if with_age:
                        return item[0], item[1]
                    return item[0]
                del self[key]
            if default is None:
                raise KeyError(key)
            elif with_age:
                return default, self.frame
            return default

    def get(self, key, default=None, with_age=False):
        """ Return the value for key if key is in dict, else default """
        with self.lock:
            if dict.__contains__(self, key):
                item = dict.__getitem__(self, key)
                if self.frame - item[1] < self.max_age:
                    if with_age:
                        return item[0], item[1]
                    return item[0]
            if default is None:
                raise KeyError(key)
            elif with_age:
                return default, self.frame
            return

    def refresh(self, key):
        with self.lock:
            if dict.__contains__(self, key):
                _item = dict.__getitem__(self, key)
                dict.__setitem__(self, key, (_item[0], self.frame))

    def items(self) -> Iterable:
        """ Return iterator of zipped list [keys, values] """
        with self.lock:
            for key, value in dict.items(self):
                if self.frame - value[1] < self.max_age:
                    yield key, value[0]

    def keys(self) -> Iterable:
        """ Return iterator of keys """
        with self.lock:
            for key, value in dict.items(self):
                if self.frame - value[1] < self.max_age:
                    yield key

    def values(self) -> Iterable:
        """ Return iterator of values """
        with self.lock:
            for value in dict.values(self):
                if self.frame - value[1] < self.max_age:
                    yield value[0]
