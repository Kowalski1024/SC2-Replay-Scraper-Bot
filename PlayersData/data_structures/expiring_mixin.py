from sc2.bot_ai_internal import BotAIInternal
from typing import TypeVar, MutableMapping, Iterable

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class ExpiringMixin(MutableMapping[_KT, _VT]):
    def __init__(self, bot: BotAIInternal, max_age_frames: int = 1):
        super().__init__()
        self._bot = bot
        self.max_age = max_age_frames

    @property
    def frame(self) -> int:
        return self._bot.state.game_loop

    def __getitem__(self, key: _KT) -> _VT:
        item = super().__getitem__(key)
        if self.frame - item[1] < self.max_age:
            return item[0]
        else:
            del self[key]
            raise KeyError(key)

    def __setitem__(self, key: _KT, value: _VT) -> None:
        super().__setitem__(key, (value, self.frame))

    def __contains__(self, key: _KT) -> bool:
        try:
            item = super().__getitem__(key)
        except KeyError:
            return False

        if self.frame - item[1] < self.max_age:
            return True
        else:
            del self[key]

        return False

    def __iter__(self) -> Iterable[_KT]:
        for key in super().__iter__():
            item = super().__getitem__(key)
            if self.frame - item[1] < self.max_age:
                yield key

    def __len__(self) -> int:
        return super().__len__()

    def __delitem__(self, key: _KT) -> None:
        super().__delitem__(key)

    def get(self, key: _KT, default: _VT = None) -> _VT:
        try:
            item = super().__getitem__(key)
            if self.frame - item[1] < self.max_age:
                return item[0]
        except KeyError:
            pass

        if default is None:
            raise KeyError(key)

        return default

    def refresh(self, key: _KT) -> None:
        item = super().__getitem__(key)
        self.__setitem__(key, (item[0], self.frame))

    def age(self, key: _KT) -> int:
        item = super().__getitem__(key)
        return item[1]
