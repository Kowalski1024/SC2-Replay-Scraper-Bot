from typing import Dict

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race

unit_label: Dict[UnitTypeId, int] = {
    UnitTypeId.PROBE: 0,
    UnitTypeId.ZEALOT: 1,
    UnitTypeId.STALKER: 2,
    UnitTypeId.SENTRY: 3,
    UnitTypeId.ADEPT: 4,
    UnitTypeId.HIGHTEMPLAR: 5,
    UnitTypeId.DARKTEMPLAR: 6,
    UnitTypeId.IMMORTAL: 7,
    UnitTypeId.COLOSSUS: 8,
    UnitTypeId.DISRUPTOR: 9,
    UnitTypeId.ARCHON: 10,
    UnitTypeId.OBSERVER: 11,
    UnitTypeId.WARPPRISM: 12,
    UnitTypeId.PHOENIX: 13,
    UnitTypeId.VOIDRAY: 14,
    UnitTypeId.ORACLE: 15,
    UnitTypeId.CARRIER: 16,
    UnitTypeId.TEMPEST: 17,
    UnitTypeId.MOTHERSHIP: 18
}

structure_label: Dict[UnitTypeId, int] = {
    # 0 - NEXUS on expansion position
    UnitTypeId.NEXUS: 1,
    UnitTypeId.PYLON: 2,
    UnitTypeId.ASSIMILATOR: 3,
    UnitTypeId.GATEWAY: 4,
    UnitTypeId.FORGE: 5,
    UnitTypeId.CYBERNETICSCORE: 6,
    UnitTypeId.PHOTONCANNON: 7,
    UnitTypeId.SHIELDBATTERY: 8,
    UnitTypeId.ROBOTICSFACILITY: 9,
    UnitTypeId.STARGATE: 10,
    UnitTypeId.TWILIGHTCOUNCIL: 11,
    UnitTypeId.ROBOTICSBAY: 12,
    UnitTypeId.FLEETBEACON: 13,
    UnitTypeId.TEMPLARARCHIVE: 14,
    UnitTypeId.DARKSHRINE: 15
}

upgrade_label: Dict[UpgradeId, int] = {
    # 0 - Ground attack
    # 1 - Flyer attack
    # 2 - Ground armor
    # 3 - Flyer armor
    # 4 - Shield armor
    UpgradeId.CHARGE: 5,
    UpgradeId.OBSERVERGRAVITICBOOSTER: 6,
    UpgradeId.GRAVITICDRIVE: 7,
    UpgradeId.VOIDRAYSPEEDUPGRADE: 8,
    UpgradeId.ADEPTPIERCINGATTACK: 9,
    UpgradeId.PHOENIXRANGEUPGRADE: 10,
    UpgradeId.EXTENDEDTHERMALLANCE: 11,
    UpgradeId.PSISTORMTECH: 12,
    UpgradeId.BLINKTECH: 13,
    UpgradeId.DARKTEMPLARBLINKUPGRADE: 14,
    UpgradeId.WARPGATERESEARCH: 15,
    UpgradeId.TEMPESTGROUNDATTACKUPGRADE: 16
}

available_labels = set(unit_label.keys()) | set(structure_label.keys()) | set(upgrade_label.keys())

state_len: Dict[Race, int] = {
    Race.Terran: 8,
    Race.Zerg: 8,
    Race.Protoss: 6
}

unit_alias: Dict[UnitTypeId, UnitTypeId] = {
    # Protoss
    UnitTypeId.OBSERVERSIEGEMODE: UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISMPHASING: UnitTypeId.WARPPRISM,
    UnitTypeId.WARPGATE: UnitTypeId.GATEWAY
}
