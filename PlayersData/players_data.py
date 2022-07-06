from typing import Union
from collections import Counter

from sc2.bot_ai import BotAI
from sc2.observer_ai import ObserverAI
from sc2.unit import Unit
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

from PlayersData.Races.protoss import AllianceProtoss, EnemyProtoss
from PlayersData.labels.abilities import abilities_dict
from PlayersData.cache import property_cache_once_per_frame
from PlayersData.labels import Labels


class PlayersData:
    def __init__(self, bot: Union[BotAI, ObserverAI]):
        self._bot = bot
        alliance_race = AllianceProtoss
        self.enemy = EnemyProtoss(bot)
        self.alliance = alliance_race(bot)
        self._prev_abilities = Counter()

    def on_prepare_step(self):
        self.alliance.update()
        self.enemy.update()

    def after_step(self):
        self.alliance.prev_state = self._bot.state

    async def on_unit_destroyed(self, tag: int):
        if self.enemy.has_unit(tag):
            self.enemy.on_unit_destroyed(tag)
        if self.alliance.has_unit(tag):
            self.alliance.on_unit_destroyed(tag)

    @property
    def state_data(self):
        def closest_distance_normalized(units):
            closest_unit = closest_unit_to_main(units)
            if closest_unit is None:
                return 1
            return round(distance_to_main(closest_unit.position) /
                         distance_to_main(self._bot.enemy_start_locations[0]), 1)

        def closest_unit_to_main(units):
            if not units:
                return None
            return units.closest_to(self._bot.start_location)

        def distance_to_main(target: Point2) -> float:
            return self._bot.start_location.distance_to_point2(target)

        common = self.alliance.prev_state.common
        unit_distance = closest_distance_normalized(
            self.enemy.units.exclude_type({UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE})
        )
        structure_distance = closest_distance_normalized(self._bot.enemy_structures)
        return {
            Labels.MINERALS.value: common.minerals,
            Labels.VESPENE.value: common.vespene,
            Labels.FOOD_LEFT.value: common.food_cap - common.food_used,
            Labels.FOOD_USED.value: common.food_used,
            Labels.UNIT_DISTANCE.value: unit_distance,
            Labels.STRUCTURE_DISTANCE.value: structure_distance
        }

    @property_cache_once_per_frame
    def get_learning_data(self):
        vec = [0] * (80 + 64)

        alliance = self.alliance.data_dict
        enemy = self.enemy.data_dict
        for key, val in (alliance | self.state_data).items():
            vec[key] = val
        for key, val in enemy.items():
            vec[key + 64] = val

        for ability, value in self.creation_orders.items():
            vec[Labels.get_value(ability)] += value
        return vec

    @property_cache_once_per_frame
    def all_orders(self) -> Counter:
        abilities_amount = Counter()
        unit: Unit
        for unit in self._bot.units | self._bot.structures:
            for order in unit.orders:
                abilities_amount[order.ability.id] += 1
            if not unit.is_ready and not unit.is_structure:
                abilities_amount[self._bot.game_data.units[unit.type_id.value].creation_ability.id] += 1
        return abilities_amount

    @property_cache_once_per_frame
    def new_orders(self) -> Counter:
        orders: Counter = self.all_orders - self._prev_abilities
        self._prev_abilities = self.all_orders
        return orders

    @property
    def creation_orders(self) -> dict:
        return {abilities_dict[x]: count for x, count in self.all_orders.items() if x in abilities_dict}

    @property
    def new_train_orders(self) -> dict:
        return {abilities_dict[x]: count for x, count in self.new_orders.items() if x in abilities_dict}
