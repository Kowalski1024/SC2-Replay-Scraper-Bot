from typing import Iterable
from collections import defaultdict
from itertools import chain

from sc2.bot_ai_internal import BotAIInternal

from bot.ids.abilities import ABILITIES_MAPPING
from bot.cache import cache_once_per_frame
from bot.utils import debug_text_mapping


class OrderCounter:
    def __init__(self, bot: BotAIInternal):
        self._bot = bot
        self.prev_orders = {}

    @cache_once_per_frame
    def all_orders(self) -> dict:
        orders = defaultdict(int)

        for unit in chain(self._bot.units, self._bot.structures):
            for order in unit.orders:
                orders[order.ability.id] += 1
            if not (unit.is_ready or unit.is_structure):
                orders[self._bot.game_data.units[unit.type_id.value].creation_ability.id] += 1

        return orders

    @cache_once_per_frame
    def new_orders(self) -> dict:
        all_orders = self.all_orders()
        orders = {order: max(0, all_orders[order] - self.prev_orders.get(order, 0)) for order in all_orders}
        self.prev_orders = all_orders

        return orders

    def creation_order(self) -> dict:
        return {ABILITIES_MAPPING[order]: val for order, val in self.all_orders().items() if order in ABILITIES_MAPPING}

    def new_creation_order(self) -> dict:
        return {ABILITIES_MAPPING[order]: val for order, val in self.new_orders().items() if order in ABILITIES_MAPPING}

    def debug_text(self, pos, creation_only=False):
        orders = self.creation_order() if creation_only else self.all_orders()
        debug_text_mapping(self._bot, mapping=orders, pos=pos, name='ORDERS')



