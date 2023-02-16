from typing import Mapping, Sequence
from collections import ChainMap
import pandas as pd

from sc2.bot_ai import BotAI
from sc2.observer_ai import ObserverAI
from sc2.unit import Unit
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

from bot.extension import BotExtension
from bot.counter.units_counter import StructureCounter, UnitsCounter
from bot.counter.order_counter import OrderCounter
from bot.ids.units import RACE_MAPPING
from bot.cache import cache_once_per_frame


class BotCounter(BotExtension):
    def __init__(self, bot: BotAI | ObserverAI):
        self._bot = bot
        self._prev_state = None
        self.structures = StructureCounter(bot)
        self.units = UnitsCounter(bot)
        self.orders = OrderCounter(bot)

    async def on_start(self):
        self._prev_state = self._bot.state

    async def on_unit_destroyed(self, unit_tag: int):
        self.units.on_unit_destroyed(unit_tag)

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        self.units.on_enemy_unit_entered_vision(unit)

    async def after_step(self, iteration: int):
        self._prev_state = self._bot.state

    @cache_once_per_frame
    def features_set(self) -> dict:
        chainmap = ChainMap(self.units.alliance(), self.structures.alliance())
        ally = {
            f'ALLY_{key.name}': chainmap.get(key, 0) for key in RACE_MAPPING[self._bot.race]
        }

        chainmap = ChainMap(self.units.enemy(), self.structures.enemy())
        enemy = {
            f'ENEMY_{key.name}': chainmap.get(key, 0) for key in RACE_MAPPING[self._bot.race]
        }

        return self._additional_data() | ally | enemy

    def _additional_data(self):
        def closest_distance_normalized(units):
            closest_unit = closest_unit_to_main(units)
            if closest_unit is None:
                return 1
            return distance_to_main(closest_unit.position) / distance_to_main(self._bot.enemy_start_locations[0])

        def closest_unit_to_main(units):
            if not units:
                return None
            return units.closest_to(self._bot.start_location)

        def distance_to_main(target: Point2) -> float:
            return self._bot.start_location.distance_to_point2(target)

        common = self._prev_state.common
        unit_distance = closest_distance_normalized(
            self._bot.enemy_units.exclude_type(
                {UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE, UnitTypeId.DRONEBURROWED}
            )
        )
        structure_distance = closest_distance_normalized(self._bot.enemy_structures)

        return {
            'MINERALS': common.minerals,
            'VESPENE': common.vespene,
            'SUPPLY_LEFT': common.food_cap - common.food_used,
            'SUPPLY_USED': common.food_used,
            'CLOSEST_UNIT': unit_distance,
            'CLOSEST_STRUCTURE': structure_distance
        }

    @staticmethod
    def _series(data: Mapping, indexes: Sequence, prefix='') -> pd.Series:
        return pd.Series(data=data, index=indexes, dtype=float).add_prefix(prefix).fillna(value=0)

    def debug_text(self, start=Point2((0.01, 0.01)), creation_only=False):
        pd.set_option("display.precision", 3)
        self.units.debug_text(start)
        self.structures.debug_text(start + Point2((0.2, 0)))
        self.orders.debug_text(Point2(start + Point2((0.48, 0))), creation_only=creation_only)
