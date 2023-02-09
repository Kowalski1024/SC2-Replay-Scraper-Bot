from typing import Optional, Iterable, Callable
from collections import Counter

from loguru import logger

from sc2.bot_ai import BotAI
from sc2.observer_ai import ObserverAI
from sc2.unit import Unit
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

from bot.ids.units import ALL_UNITS, ALL_STRUCTURES, CORRECT_ALIAS


class UnitsCounter:
    def __init__(self, bot: BotAI | ObserverAI) -> None:
        self._bot = bot
        self._seen_enemy_tags: dict[int, UnitTypeId] = {}
        self._enemy_units_counter = Counter()
        self._enemy_units_handlers: dict[Race, Callable] = {
            Race.Terran: self._terran_handler,
            Race.Zerg: self._zerg_handler,
            Race.Protoss: self._protoss_handler
        }

    def on_enemy_unit_entered_vision(self, unit: Unit) -> None:
        unit_type = self.correct_type_id(unit)

        if unit_type is None or unit_type not in ALL_UNITS:
            return None

        try:
            if (prev_type := self._seen_enemy_tags[unit.tag]) == unit_type:
                return None

            self._sub_from_counter(self._enemy_units_counter, prev_type)
            self._enemy_units_counter[unit_type] += 1
            logger.info(f"Enemy unit change type from {prev_type} to {unit_type}")
        except KeyError:
            handler = self._enemy_units_handlers[self._bot.enemy_race]
            handler(unit_type, self._enemy_units_counter)
            logger.info(f"Added {unit_type} to enemy counter")
        finally:
            self._seen_enemy_tags[unit.tag] = unit_type

    def on_unit_destroyed(self, tag: int) -> None:
        try:
            unit_type = self._seen_enemy_tags.pop(tag)
        except KeyError:
            return None

        self._sub_from_counter(self._enemy_units_counter, unit_type)

    def enemy_structures(self) -> Counter:
        return Counter(self.units_type_id(self._bot.enemy_structures))

    def enemy_units(self) -> Counter:
        return self._enemy_units_counter

    def alliance_structures(self) -> Counter:
        return Counter(self.units_type_id(self._bot.structures))

    def alliance_units(self) -> Counter:
        return Counter(self.units_type_id(self._bot.units))

    @staticmethod
    def correct_type_id(unit: Unit) -> Optional[UnitTypeId]:
        unit_type = CORRECT_ALIAS.get(unit.type_id, unit.type_id)

        return unit_type if unit_type in ALL_UNITS else None

    @staticmethod
    def units_type_id(units: Iterable[Unit]):
        for unit in units:
            unit_type = CORRECT_ALIAS.get(unit.type_id, unit.type_id)
            if unit_type in ALL_UNITS or unit_type in ALL_STRUCTURES:
                yield unit_type

    @staticmethod
    def _sub_from_counter(counter: Counter, key):
        if counter[key] > 0:
            counter[key] -= 1
            logger.info(f"Subtract {key} from enemy counter")
        else:
            logger.warning(f"Attempting to subtract from zero: {key}")

    @staticmethod
    def _terran_handler(unit_type: UnitTypeId, counter: Counter):
        counter[unit_type] += 1

    @staticmethod
    def _zerg_handler(unit_type: UnitTypeId, counter: Counter):
        counter[unit_type] += 1

    @staticmethod
    def _protoss_handler(unit_type: UnitTypeId, counter: Counter):
        counter[unit_type] += 1
