import csv
from observer_ai import ObserverAI
from sc2.units import Unit, Units
from collections import Counter
from sc2.cache import property_cache_once_per_frame
from constants import building_abilities, train_abilities, abilities_set
from PlayersData.constants import unit_label, structure_label
from PlayersData.players_data import PlayersData
from sc2.data import Race
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId
from pprint import pprint


class ObserverBot(ObserverAI):
    def __init__(self, file_name: str):
        super().__init__()
        self._file_name = file_name
        self.iteration = 0
        self._prev_abilities = Counter()
        self.players_data = PlayersData(self)

    async def on_unit_destroyed(self, unit_tag: int):
        await self.players_data.on_unit_destroyed(unit_tag)

    async def on_start(self):
        print("Game started")

    def on_prepare_step(self):
        self.players_data.on_prepare_step()

    def after_step(self):
        self.players_data.after_step()

    async def on_step(self, iteration):
        self.on_prepare_step()
        self.iteration = iteration
        if self.players_data.new_train_orders:
            with open('data/datasets/'+self._file_name+'.csv', 'a', encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.players_data.train_data)
        self.after_step()

    def on_end(self, result):
        print("Game ended.")
