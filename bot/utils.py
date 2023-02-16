from typing import Iterable, Optional, MutableMapping, Any
import pandas as pd

from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sc2.bot_ai_internal import BotAIInternal
from sc2.position import Point2

from bot.ids.units import CORRECT_ALIAS, ALL_UNITS, ALL_STRUCTURES


def correct_type_id(unit: Unit) -> Optional[UnitTypeId]:
    unit_type = CORRECT_ALIAS.get(unit.type_id, unit.type_id)

    return unit_type if unit_type in ALL_UNITS else None


def units_type_id(units: Iterable[Unit]):
    for unit in units:
        unit_type = CORRECT_ALIAS.get(unit.type_id, unit.type_id)
        if unit_type in ALL_UNITS or unit_type in ALL_STRUCTURES:
            yield unit_type


def debug_text_mapping(bot: BotAIInternal, mapping: MutableMapping[Any, float], pos: Point2, size=16, name=''):
    s = pd.Series(data=mapping, index=mapping.keys(), dtype=float).fillna(value=0)
    bot.client.debug_text_screen(f'{name}\n{s}', pos=pos, size=size)
