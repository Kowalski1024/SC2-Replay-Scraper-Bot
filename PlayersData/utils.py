from typing import Union, Optional

import sc2.unit
from sc2.position import Point2
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

from PlayersData.constants import unit_alias, unit_label, structure_label, upgrade_label


def get_label(u: Union[UnitTypeId, UpgradeId, sc2.unit.Unit], /):
    if isinstance(u, sc2.unit.Unit):
        u = u.type_id
    if u in upgrade_label:
        return upgrade_label[u]
    else:
        _type = unit_alias.get(u, u)
        return unit_label[_type] if _type in unit_label else structure_label[_type]


def correct_type(unit: sc2.unit.Unit):
    _type = unit.type_id
    return unit_alias.get(_type, _type)


def townhall_is_expansion(unit: sc2.unit.Unit, expansions: list[Point2]):
    for exp in expansions:
        if exp.distance_to(unit) < 1:
            return True
    return False

