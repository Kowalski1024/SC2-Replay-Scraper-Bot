from sc2.bot_ai import BotAI
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2

from .interface import EnemyData, AllianceData
from PlayersData.unit import Unit
from PlayersData.utils import get_label, correct_type, townhall_is_expansion
from PlayersData.constants import available_labels


class AllianceProtoss(AllianceData):
    def __init__(self, bot: BotAI):
        super().__init__(bot)

    def update(self):
        self.structures = self._bot.structures
        for unit in self._bot.units:
            tag = unit.tag
            if tag in self.units:
                self.units[tag].update(unit)
            else:
                unit_type = correct_type(unit)
                if unit_type in available_labels:
                    self._unit_types[unit_type].add(tag)
                    self.units[tag] = Unit(unit)
                    self._units_vector[get_label(unit_type)] += 1

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
        unit_type = correct_type(self.units[tag])
        self._units_vector[get_label(unit_type)] -= 1
        self.units.pop(tag)
        self._unit_types[unit_type].remove(tag)


class EnemyProtoss(EnemyData):
    def __init__(self, bot: BotAI):
        super().__init__(bot)

    def update(self):
        self.structures = self._bot.enemy_structures
        for unit in self._bot.enemy_units:
            tag = unit.tag
            if tag in self._units:
                self._units[tag].update(unit)
                self._units.refresh(tag)
            else:
                unit_type = correct_type(unit)
                if unit_type in available_labels:
                    self._unit_types[unit_type].add(tag)
                    self._units[tag] = Unit(unit)
                    if tag not in self._units_tags:
                        self._units_vector[get_label(unit_type)] += 1
                        if unit_type == UnitTypeId.ARCHON:
                            if self._units_vector[get_label(UnitTypeId.HIGHTEMPLAR)] >= 2:
                                self._units_vector[get_label(UnitTypeId.HIGHTEMPLAR)] -= 2
                            elif self._units_vector[get_label(UnitTypeId.DARKTEMPLAR)] >= 2:
                                self._units_vector[get_label(UnitTypeId.DARKTEMPLAR)] -= 2
                    self._units_tags.add(tag)

    def on_unit_destroyed(self, tag: int):
        unit_type = correct_type(self._units[tag])
        self._units_vector[get_label(unit_type)] -= 1
        self._units.pop(tag)
        self._unit_types[unit_type].remove(tag)
