from sc2.ids.unit_typeid import UnitTypeId
from sc2.data import Race


CORRECT_ALIAS: dict[UnitTypeId, UnitTypeId] = {
    # Protoss
    UnitTypeId.OBSERVERSIEGEMODE: UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISMPHASING: UnitTypeId.WARPPRISM,
    UnitTypeId.WARPGATE: UnitTypeId.GATEWAY
}


PROTOSS_UNITS: tuple[UnitTypeId, ...] = (
    UnitTypeId.PROBE,
    UnitTypeId.ZEALOT,
    UnitTypeId.STALKER,
    UnitTypeId.SENTRY,
    UnitTypeId.ADEPT,
    UnitTypeId.HIGHTEMPLAR,
    UnitTypeId.DARKTEMPLAR,
    UnitTypeId.IMMORTAL,
    UnitTypeId.COLOSSUS,
    UnitTypeId.DISRUPTOR,
    UnitTypeId.ARCHON,
    UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISM,
    UnitTypeId.PHOENIX,
    UnitTypeId.VOIDRAY,
    UnitTypeId.ORACLE,
    UnitTypeId.CARRIER,
    UnitTypeId.TEMPEST,
    UnitTypeId.MOTHERSHIP,
)


PROTOSS_STRUCTURES: tuple[UnitTypeId, ...] = (
    UnitTypeId.NEXUS,
    UnitTypeId.PYLON,
    UnitTypeId.ASSIMILATOR,
    UnitTypeId.GATEWAY,
    UnitTypeId.FORGE,
    UnitTypeId.CYBERNETICSCORE,
    UnitTypeId.PHOTONCANNON,
    UnitTypeId.SHIELDBATTERY,
    UnitTypeId.ROBOTICSFACILITY,
    UnitTypeId.STARGATE,
    UnitTypeId.TWILIGHTCOUNCIL,
    UnitTypeId.ROBOTICSBAY,
    UnitTypeId.FLEETBEACON,
    UnitTypeId.TEMPLARARCHIVE,
    UnitTypeId.DARKSHRINE,
)

RACE_MAPPING: dict[Race, tuple[UnitTypeId]] = {
    Race.Protoss: PROTOSS_UNITS + PROTOSS_STRUCTURES
}

ALL_UNITS: set[UnitTypeId] = {*PROTOSS_UNITS}
ALL_STRUCTURES: set[UnitTypeId] = {*PROTOSS_STRUCTURES}
