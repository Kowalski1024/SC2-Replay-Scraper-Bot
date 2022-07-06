from typing import Union

from sc2.bot_ai_internal import BotAIInternal
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2

from .base import EnemyData, AllianceData
from PlayersData.unit import Unit
from PlayersData.utils import correct_type, townhall_is_expansion
from ..labels import alias, Labels


class AllianceProtoss(AllianceData):
    def __init__(self, bot):
        super().__init__(bot)

    def update(self):
        for unit in self._bot.units:
            tag = unit.tag
            if tag in self._units:
                self._units[tag].update(unit)
            else:
                unit_type = correct_type(unit)
                self._unit_types[unit_type].add(tag)
                self._units[tag] = Unit(unit)
                if unit_type in alias:
                    self._data_dict[Labels.get_value(unit_type)] += 1

    # TODO: self.state.upgrades
    # def on_upgrade_complete(self, upgrade: UpgradeId):
    #     if upgrade in {
    #         UpgradeId.PROTOSSSHIELDSLEVEL1,
    #         UpgradeId.PROTOSSSHIELDSLEVEL2,
    #         UpgradeId.PROTOSSSHIELDSLEVEL3
    #     }:
    #         self._upgrades_vector[4] = upgrade.value - UpgradeId.PROTOSSSHIELDSLEVEL1.value + 1
    #     elif upgrade in {
    #         UpgradeId.PROTOSSAIRARMORSLEVEL1,
    #         UpgradeId.PROTOSSAIRARMORSLEVEL2,
    #         UpgradeId.PROTOSSAIRARMORSLEVEL3
    #     }:
    #         self._upgrades_vector[3] = upgrade.value - UpgradeId.PROTOSSAIRARMORSLEVEL1.value + 1
    #     elif upgrade in {
    #         UpgradeId.PROTOSSAIRWEAPONSLEVEL1,
    #         UpgradeId.PROTOSSAIRWEAPONSLEVEL2,
    #         UpgradeId.PROTOSSAIRWEAPONSLEVEL3
    #     }:
    #         self._upgrades_vector[2] = upgrade.value - UpgradeId.PROTOSSAIRWEAPONSLEVEL1.value + 1
    #     elif upgrade in {
    #         UpgradeId.PROTOSSGROUNDARMORSLEVEL1,
    #         UpgradeId.PROTOSSGROUNDARMORSLEVEL2,
    #         UpgradeId.PROTOSSGROUNDARMORSLEVEL3
    #     }:
    #         self._upgrades_vector[1] = upgrade.value - UpgradeId.PROTOSSGROUNDARMORSLEVEL1.value + 1
    #     elif upgrade in {
    #         UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1,
    #         UpgradeId.PROTOSSGROUNDWEAPONSLEVEL2,
    #         UpgradeId.PROTOSSGROUNDWEAPONSLEVEL3
    #     }:
    #         self._upgrades_vector[0] = upgrade.value - UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1.value + 1
    #     else:
    #         self._upgrades_set.add(upgrade)
    #         self._upgrades_vector[get_label(upgrade)] = 1

    def on_unit_destroyed(self, tag: int):
        unit_type = correct_type(self._bot._units_previous_map[tag])
        self._units.pop(tag)
        self._unit_types[unit_type].remove(tag)

        if unit_type in alias:
            self._data_dict[Labels.get_value(unit_type)] -= 1


class EnemyProtoss(EnemyData):
    def __init__(self, bot):
        super().__init__(bot)

    def update(self):
        for unit in self.visible_units:
            tag = unit.tag
            if tag in self._units:
                self._units[tag].update(unit)
                self._units.refresh(tag)
            else:
                unit_type = correct_type(unit)
                self._units[tag] = Unit(unit)
                self._unit_types[unit_type].add(tag)
                if unit_type in alias:
                    if tag not in self._seen_units:
                        self._data_dict[Labels.get_value(unit_type)] += 1
                        # if unit_type == UnitTypeId.ARCHON:
                        #     if self._vector_dict[Labels.HIGHTEMPLAR] >= 2:
                        #         self._vector_dict[Labels.HIGHTEMPLAR] -= 2
                        #     elif self._vector_dict[Labels.DARKTEMPLAR] >= 2:
                        #         self._vector_dict[Labels.DARKTEMPLAR] -= 2
            self._seen_units[tag] = unit

    def on_unit_destroyed(self, tag: int):
        unit_type = correct_type(self._seen_units[tag])
        self._units.pop(tag)
        self._unit_types[unit_type].remove(tag)
        del self._seen_units[tag]

        if unit_type in alias:
            self._data_dict[Labels.get_value(unit_type)] -= 1
