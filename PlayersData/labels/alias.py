from PlayersData.data_structures.two_way_dict import TwoWayDict
from ..labels import Labels
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId


alias = TwoWayDict({
    # PROTOSS
    # Units
    Labels.PROBE: UnitTypeId.PROBE,
    Labels.ZEALOT: UnitTypeId.ZEALOT,
    Labels.STALKER: UnitTypeId.STALKER,
    Labels.SENTRY: UnitTypeId.SENTRY,
    Labels.ADEPT: UnitTypeId.ADEPT,
    Labels.HIGHTEMPLAR: UnitTypeId.HIGHTEMPLAR,
    Labels.DARKTEMPLAR: UnitTypeId.DARKTEMPLAR,
    Labels.IMMORTAL: UnitTypeId.IMMORTAL,
    Labels.COLOSSUS: UnitTypeId.COLOSSUS,
    Labels.DISRUPTOR: UnitTypeId.DISRUPTOR,
    Labels.ARCHON: UnitTypeId.ARCHON,
    Labels.OBSERVER: UnitTypeId.OBSERVER,
    Labels.WARPPRISM: UnitTypeId.WARPPRISM,
    Labels.PHOENIX: UnitTypeId.PHOENIX,
    Labels.VOIDRAY: UnitTypeId.VOIDRAY,
    Labels.ORACLE: UnitTypeId.ORACLE,
    Labels.CARRIER: UnitTypeId.CARRIER,
    Labels.TEMPEST: UnitTypeId.TEMPEST,
    Labels.MOTHERSHIP: UnitTypeId.MOTHERSHIP,

    # Structures
    Labels.NEXUS: UnitTypeId.NEXUS,
    Labels.PYLON: UnitTypeId.PYLON,
    Labels.ASSIMILATOR: UnitTypeId.ASSIMILATOR,
    Labels.GATEWAY: UnitTypeId.GATEWAY,
    Labels.FORGE: UnitTypeId.FORGE,
    Labels.CYBERNETICSCORE: UnitTypeId.CYBERNETICSCORE,
    Labels.PHOTONCANNON: UnitTypeId.PHOTONCANNON,
    Labels.SHIELDBATTERY: UnitTypeId.SHIELDBATTERY,
    Labels.ROBOTICSFACILITY: UnitTypeId.ROBOTICSFACILITY,
    Labels.STARGATE: UnitTypeId.STARGATE,
    Labels.TWILIGHTCOUNCIL: UnitTypeId.TWILIGHTCOUNCIL,
    Labels.ROBOTICSBAY: UnitTypeId.ROBOTICSBAY,
    Labels.FLEETBEACON: UnitTypeId.FLEETBEACON,
    Labels.TEMPLARARCHIVE: UnitTypeId.TEMPLARARCHIVE,
    Labels.DARKSHRINE: UnitTypeId.DARKSHRINE,

    # Upgrades
    Labels.CHARGE: UpgradeId.CHARGE,
    Labels.OBSERVERGRAVITICBOOSTER: UpgradeId.OBSERVERGRAVITICBOOSTER,
    Labels.GRAVITICDRIVE: UpgradeId.GRAVITICDRIVE,
    Labels.VOIDRAYSPEEDUPGRADE: UpgradeId.VOIDRAYSPEEDUPGRADE,
    Labels.ADEPTPIERCINGATTACK: UpgradeId.ADEPTPIERCINGATTACK,
    Labels.PHOENIXRANGEUPGRADE: UpgradeId.PHOENIXRANGEUPGRADE,
    Labels.EXTENDEDTHERMALLANCE: UpgradeId.EXTENDEDTHERMALLANCE,
    Labels.PSISTORMTECH: UpgradeId.PSISTORMTECH,
    Labels.BLINKTECH: UpgradeId.BLINKTECH,
    Labels.DARKTEMPLARBLINKUPGRADE: UpgradeId.DARKTEMPLARBLINKUPGRADE,
    Labels.WARPGATERESEARCH: UpgradeId.WARPGATERESEARCH,
    Labels.TEMPESTGROUNDATTACKUPGRADE: UpgradeId.TEMPESTGROUNDATTACKUPGRADE
})

correct_alias: dict[UnitTypeId, UnitTypeId] = {
    # Protoss
    UnitTypeId.OBSERVERSIEGEMODE: UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISMPHASING: UnitTypeId.WARPPRISM,
    UnitTypeId.WARPGATE: UnitTypeId.GATEWAY
}

