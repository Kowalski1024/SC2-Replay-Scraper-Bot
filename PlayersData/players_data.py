from typing import Union
from collections import Counter

from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.observer_ai import ObserverAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

from PlayersData.Races.protoss import AllianceProtoss, EnemyProtoss
from constants import building_abilities, train_abilities, abilities_set
from PlayersData.constants import unit_label, structure_label
from PlayersData.cache import property_cache_once_per_frame


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
        if tag in self.enemy._units:
            self.enemy.on_unit_destroyed(tag)
        if tag in self.alliance.units:
            self.alliance.on_unit_destroyed(tag)

    @property
    def state_vector(self):
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
        state = [
            common.minerals, common.vespene, common.food_cap - common.food_used, common.food_used,
            closest_distance_normalized(
                self.enemy.units.exclude_type({UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE})
            ),
            closest_distance_normalized(self._bot.enemy_structures)
        ]
        return state

    @property_cache_once_per_frame
    def get_learning_data(self):
        alliance = self.alliance.units_vector + self.alliance.structures_vector
        enemy = self.enemy.units_vector + self.enemy.structures_vector
        return self.state_vector + alliance + enemy

    @property_cache_once_per_frame
    def all_orders(self) -> Counter:
        abilities_amount = Counter()
        unit: Unit
        for unit in self._bot.units + self._bot.structures:
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

    @property_cache_once_per_frame
    def new_train_orders(self) -> dict:
        return {x: count for x, count in self.new_orders.items() if x in abilities_set}

    @property
    def action_vector(self):
        buildings = [0] * 24
        trains = [0] * 24
        orders = self.new_train_orders
        for ability, value in orders.items():
            if ability in building_abilities:
                buildings[structure_label[building_abilities[ability]]] = value
            else:
                trains[unit_label[train_abilities[ability]]] = value
        return trains, buildings

    @property
    def train_data(self):
        actions = self.action_vector
        return self.get_learning_data + actions[0] + actions[1]
