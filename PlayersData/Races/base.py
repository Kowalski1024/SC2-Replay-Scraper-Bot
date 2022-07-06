from collections import defaultdict
from typing import DefaultDict, Optional, Union

from sc2.bot_ai import BotAI
from sc2.observer_ai import ObserverAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sc2.position import Point2
from sc2.data import race_townhalls, Race

from PlayersData.data_structures.expiring_dict import ExpiringDict
from PlayersData.labels import Labels
from PlayersData.unit import Unit
from PlayersData.cache import property_cache_once_per_frame


class PlayerData:
    def __init__(self, bot_ai: Union[BotAI, ObserverAI]):
        self._bot = bot_ai
        self._units: Optional[dict] = None
        self._unit_types: DefaultDict[UnitTypeId, set[int]] = defaultdict(set)
        self._data_dict = {label.value: 0 for label in Labels}
        self._upgrades_set = set()

    @property_cache_once_per_frame
    def units(self) -> Units:
        return Units(self._units.values(), self._bot)

    def has_unit(self, tag: int):
        return tag in self._units

    @property
    def structures(self) -> Units:
        return Units([], self._bot)

    @property
    def data_dict(self):
        self.update_structures()
        return self._data_dict.copy()

    def update(self):
        pass

    def on_unit_destroyed(self, unit_tag: int):
        pass

    def update_structures(self):
        structures = dict()
        self._data_dict[Labels.EXPANSIONS.value] = 0
        for unit in self.structures:
            if unit.build_progress > 0.01:
                val = structures.get(Labels.get_value(unit), 0)
                structures[Labels.get_value(unit)] = val + 1
            if (
                    unit.type_id in race_townhalls[Race.Random]
                    and any(exp.distance_to(unit) < 1 for exp in self._bot.expansion_locations_list)
            ):
                self._data_dict[Labels.EXPANSIONS.value] += 1
        self._data_dict.update(structures)

    @property
    def upgrades_set(self):
        return self._upgrades_set


class EnemyData(PlayerData):
    def __init__(self, bot_ai):
        super().__init__(bot_ai)
        self._units: ExpiringDict[int, Unit] = ExpiringDict(self._bot, 1000)
        self._seen_units: dict[int, Unit] = dict()

    @property
    def visible_units(self) -> Units:
        return self._bot.enemy_units

    @property
    def structures(self) -> Units:
        return self._bot.enemy_structures

    def has_unit(self, tag: int):
        return tag in self._seen_units


class AllianceData(PlayerData):
    def __init__(self, bot_ai):
        super().__init__(bot_ai)
        self._units: dict[int, Unit] = {}
        self.prev_state = None

    @property
    def structures(self) -> Units:
        return self._bot.structures
