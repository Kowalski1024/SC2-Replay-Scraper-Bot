from collections import defaultdict
from typing import DefaultDict, Union, Optional, OrderedDict

import sc2.units
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

from PlayersData.expiring_dict import ExpiringDict
from PlayersData.unit import Unit
from PlayersData.utils import correct_type, get_label, townhall_is_expansion


class PlayerData:
    def __init__(self, bot_ai: BotAI):
        self.bot = bot_ai
        self.units: Optional[sc2.units.Units] = None
        self.structures: Optional[sc2.units.Units] = None
        self._unit_types: DefaultDict[UnitTypeId, set[int]] = defaultdict(set)
        self._units_vector = [0]*24
        self._structures_vector = [0]*24
        self._upgrades_vector = [0]*24
        self._upgrades_set = set()

    async def update(self):
        pass

    def on_unit_destroyed(self, unit_tag: int):
        pass

    @property
    def units_vector(self):
        return self._units_vector

    @property
    def structures_vector(self):
        vec = self._structures_vector.copy()
        for unit in self.structures:
            _type = correct_type(unit)
            vec[get_label(_type)] += 1
            if (
                    _type in {UnitTypeId.NEXUS, UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY}
                    and townhall_is_expansion(unit, self.bot._expansion_positions_list)
            ):
                vec[0] += 1
        return vec

    @property
    def upgrades_vector(self):
        return self._upgrades_vector

    @property
    def upgrades_set(self):
        return self._upgrades_set


class EnemyData(PlayerData):
    def __init__(self, bot_ai: BotAI):
        super().__init__(bot_ai)
        self.units: ExpiringDict[int, Unit] = ExpiringDict(self.bot, 1000)
        self._units_tags = set()


class AllianceData(PlayerData):
    def __init__(self, bot_ai: BotAI):
        super().__init__(bot_ai)
        self.units: dict[int, Unit] = {}
