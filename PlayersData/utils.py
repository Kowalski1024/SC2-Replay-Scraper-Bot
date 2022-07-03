from typing import Union

import sc2.unit
from sc2.position import Point2
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

from PlayersData.labels import alias, correct_alias, Labels


def get_label(u, /) -> Union[Labels, UnitTypeId, UpgradeId]:
    if isinstance(u, sc2.unit.Unit):
        u = u.type_id
    _type = correct_alias.get(u, u)
    return alias[_type]


def correct_type(unit: sc2.unit.Unit):
    _type = unit.type_id
    return correct_alias.get(_type, _type)


def townhall_is_expansion(unit: sc2.unit.Unit, expansions: list[Point2]):
    for exp in expansions:
        if exp.distance_to(unit) < 1:
            return True
    return False

