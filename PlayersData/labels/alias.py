from sc2.ids.unit_typeid import UnitTypeId

correct_alias: dict[UnitTypeId, UnitTypeId] = {
    # Protoss
    UnitTypeId.OBSERVERSIEGEMODE: UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISMPHASING: UnitTypeId.WARPPRISM,
    UnitTypeId.WARPGATE: UnitTypeId.GATEWAY
}

