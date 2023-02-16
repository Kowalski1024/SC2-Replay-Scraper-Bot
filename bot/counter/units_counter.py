from typing import Iterable, MutableMapping
from collections import defaultdict

from sc2.bot_ai_internal import BotAIInternal
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId

from bot.ids.units import ALL_UNITS, ALL_STRUCTURES, CORRECT_ALIAS
from bot.ids.abilities import ABILITIES_MAPPING
from bot.cache import cache_once_per_frame
from bot.extension import BotExtension
from bot.utils import debug_text_mapping


class StructureCounter(BotExtension):
    def __init__(self, bot: BotAIInternal):
        self._bot = bot

    @cache_once_per_frame
    def enemy(self) -> dict:
        counter = self._count(self._bot.enemy_structures)
        return counter

    @cache_once_per_frame
    def alliance(self) -> dict:
        counter = self._count(self._bot.structures)
        return counter

    @staticmethod
    def _count(units: Iterable[Unit]) -> dict:
        counter = {}
        in_progress = {}

        for unit in units:
            unit_type = CORRECT_ALIAS.get(unit.type_id, unit.type_id)

            if unit_type in ALL_STRUCTURES:
                if unit.is_ready:
                    try:
                        counter[unit_type] += 1
                    except KeyError:
                        counter[unit_type] = 1
                else:
                    val = in_progress.get(unit_type, 0.1)
                    in_progress[unit_type] = max(val, unit.build_progress)

        for unit_type, progress in in_progress.items():
            try:
                counter[unit_type] += progress
            except KeyError:
                counter[unit_type] = progress

        return counter

    def debug_text(self, pos):
        debug_text_mapping(self._bot, mapping=self.alliance(), pos=pos, name='ALLY STRUCTURES')
        debug_text_mapping(self._bot, mapping=self.enemy(), pos=pos+(0.12, 0), name='ENEMY STRUCTURES')


class UnitsCounter:
    def __init__(self, bot: BotAIInternal):
        self._bot = bot
        self._enemy_counter = PlayerUnitsCounter(bot, max_age=8192)
        self._alliance_counter = PlayerUnitsCounter(bot, max_age=1024)

    @cache_once_per_frame
    def enemy(self) -> dict:
        return self._enemy_counter.count()

    @cache_once_per_frame
    def alliance(self) -> dict:
        for unit in self._bot.units:
            self._alliance_counter.add(unit)

        counter = self._alliance_counter.count()

        in_progress = {}
        for structure in self._bot.structures:
            for orders in structure.orders:
                try:
                    unit_type = ABILITIES_MAPPING[orders.ability.id]
                except KeyError:
                    continue

                if unit_type in ALL_UNITS:
                    val = in_progress.get(unit_type, 0)
                    in_progress[unit_type] = max(val, orders.progress)

        for key, val in in_progress.items():
            try:
                counter[key] += val
            except KeyError:
                counter[key] = val

        return counter

    def on_enemy_unit_entered_vision(self, unit: Unit) -> None:
        self._enemy_counter.add(unit)

    def on_unit_destroyed(self, tag: int) -> None:
        self._enemy_counter.remove(tag)
        self._alliance_counter.remove(tag)

    def debug_text(self, pos):
        debug_text_mapping(self._bot, mapping=self.alliance(), pos=pos, name='ALLY UNITS')
        debug_text_mapping(self._bot, mapping=self.enemy(), pos=pos+(0.1, 0), name='ENEMY UNITS')


class PlayerUnitsCounter:
    def __init__(self, bot: BotAIInternal, max_age=float('inf')):
        self._bot = bot
        self._seen_tags: dict[int, tuple[UnitTypeId, int]] = {}
        self._max_age = max_age

    def count(self) -> dict:
        counter = {}

        for unit_type, age in self._seen_tags.values():
            if self._bot.state.game_loop - age < self._max_age:
                try:
                    counter[unit_type] += 1
                except KeyError:
                    counter[unit_type] = 1

        return counter

    def add(self, unit: Unit) -> None:
        unit_type = CORRECT_ALIAS.get(unit.type_id, unit.type_id)
        if unit_type in ALL_UNITS:
            self._seen_tags[unit.tag] = unit_type, self._bot.state.game_loop

    def remove(self, tag: int) -> None:
        try:
            self._seen_tags.pop(tag)
        except KeyError:
            return

    def __contains__(self, item: int):
        return item in self._seen_tags
