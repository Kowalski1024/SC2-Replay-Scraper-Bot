from typing import Union

from sc2.bot_ai_internal import BotAIInternal
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2

from .base import EnemyData, AllianceData
from PlayersData.unit import Unit
from PlayersData.utils import correct_type
from ..labels import alias, Labels


class AllianceProtoss(AllianceData):
    def __init__(self, bot):
        super().__init__(bot)

    def update(self):
        for unit in self._bot.units:
            tag = unit.tag
            if tag not in self._seen_units:
                unit_type = correct_type(unit)
                if unit_type in alias:
                    self._data_dict[Labels.get_value(unit_type)] += 1
                self._seen_units[tag] = unit_type

    def on_unit_destroyed(self, tag: int):
        unit_type = self._seen_units[tag]
        self._seen_units.pop(tag)
        if unit_type in alias:
            self._data_dict[Labels.get_value(unit_type)] -= 1


class EnemyProtoss(EnemyData):
    def __init__(self, bot):
        super().__init__(bot)

    def update(self):
        for unit in self.visible_units:
            tag = unit.tag
            self._units[tag] = unit
            if tag not in self._seen_units:
                unit_type = correct_type(unit)
                if unit_type in alias:
                    if tag not in self._seen_units:
                        self._data_dict[Labels.get_value(unit_type)] += 1
                self._seen_units[tag] = unit_type

    def on_unit_destroyed(self, tag: int):
        unit_type = self._seen_units[tag]
        self._seen_units.pop(tag)
        if unit_type in alias:
            self._data_dict[Labels.get_value(unit_type)] -= 1
