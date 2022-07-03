from collections import deque

import sc2.unit


class Unit(sc2.unit.Unit):
    def __init__(self, unit: sc2.unit.Unit):
        super().__init__(unit._proto, unit._bot_object, unit.distance_calculation_index, unit.base_build)
        self.positions_deque = deque([unit.position], maxlen=5)

    def refresh_unit(self, unit: sc2.unit.Unit):
        self._proto = unit._proto
        self.distance_calculation_index = unit.distance_calculation_index
        self.base_build = unit.base_build
        self.game_loop = unit.game_loop

    def update(self, unit: sc2.unit.Unit):
        self.refresh_unit(unit)
        self.positions_deque.append(unit.position)
        return self
